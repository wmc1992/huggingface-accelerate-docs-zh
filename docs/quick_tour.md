# Quick tour

## 主要用法

在之前的文档 [Accelerate](./Accelerate.md) 中已经看到过要想使用Accelerate需要做的代码修改如下所示：

<div><pre><code class="language-python hljs">
<font color=green>+ from accelerate import Accelerator</font>
<span></span>
<font color=green>+ accelerator = Accelerator()</font>
<font color=red>- my_model.to(device)</font>
<font>  # Pass every important object (model, optimizer, dataloader) to `accelerator.prepare`</font>
<font color=green>+ my_model, my_optimizer, my_training_dataloader = accelerate.prepare(</font>
<font color=green>+     my_model, my_optimizer, my_training_dataloader</font>
<font color=green>+ )</font>
<span></span>
<font>  for batch in my_training_dataloader:</font>
<font>      my_optimizer.zero_grad()</font>
<font>      inputs, targets = batch</font>
<font color=red>-     inputs = inputs.to(device)</font>
<font color=red>-     targets = targets.to(device)</font>
<font>      outputs = my_model(inputs)</font>
<font>      loss = my_loss_function(outputs, targets)</font>
<font>      # Just a small change for the backward instruction</font>
<font color=red>-     loss.backward()</font>
<font color=green>+     accelerate.backward(loss)</font>
<font>      my_optimizer.step()</font>
</code></pre></div>

上述代码的修改可以分为四个步骤进行：

1. import 并实例化 Accelerator 对象，代码如下：

```python
from accelerate import Accelerator

accelerator = Accelerator()
```

上述这个初始化代码会自动检测设备和环境信息（单CPU、多CPU、单GPU、多GPU、TPU等等都会自动检测到），开发者完全不需要关心设备和环境信息。

需要注意的一点是：上述初始化代码必须要在所有训练有关的代码之前执行；

2. 删除原代码中的 `to(device)` 和 `cuda()`，Accelerator 会自动将model、data等放到正确的设备上，开发者不用关心。

当然，如果是高端玩家想要自己指定设备信息也可以，此时 `to(device)` 中的 `device` 需要是 `accelerator.device`。

最后，如果完全不想使用 Accelerator 自动管理设备的功能，可以在初始化时传入参数 `device_placement=False`，代码如下：

```python
accelerator = Accelerator(device_placement=False)
```

3. 将所有和训练相关的对象（`optimizer`, `model`, `training dataloader`）传入函数 `prepare()`。该步骤应该放在所有相关对象初始化之后，和训练开始之前。代码如下：

```
model, optimizer, train_dataloader = accelerator.prepare(model, optimizer, train_dataloader)
```

**对 `train_dataloader` 说明**：当做分布式训练时，以多GPU为例，所有的训练数据会平均分配到每个GPU上。当训练数据需要 shuffle 时，其实现原理是：

* 将随机状态（random state）同步到所有的GPU，以此保证每个GPU上训练数据 shuffle 之后的顺序是相同的；
* 每个GPU读取 shuffle 后的训练数据的不同片段；比如有2个GPU时，第一个GPU读取第 `[1, 3, 5, 7, ...]` 条数据，第二个GPU读取第 `[0, 2, 4, 6, ...]` 条数据；

**对 `batch_size` 说明**：当做分布式训练时，以多GPU为例：实际的batch_size = 输入的batch_size * GPU数量。比如输入batch_size为16，当使用4个GPU进行分布式训练时，实际的batch_size为64。

**对 `validation dataloader` 说明**：上面传入 `prepare()` 的只有 `train_dataloader`，另外 `validation dataloader` 也可以传入 `prepare()`，具体的使用方式见下面的**分布式评估**部分。

4. 将 `loss.backward()` 替换成 `accelerator.backward(loss)`。

完成以上四个步骤之后就可以正常的使用 Accelerator 了。

## 分布式评估

如果要做分布式评估，只需要将 `validation_dataloader` 也传入 `prepare()`，代码如下：

```python
validation_dataloader = accelerator.prepare(validation_dataloader)
```

和 `train_dataloader` 的实现原理类似，`validation_dataloader` 中所有的数据会被划分到多个GPU上，所以在模型前向传播完成之后要调用函数 `gather()` 做一下聚合，代码如下：

```python
for inputs, targets in validation_dataloader:
    predictions = model(inputs)
    # Gather all predictions and targets
    all_predictions = accelerator.gather(predictions)
    all_targets = accelerator.gather(targets)
    # Example of use with a `Datasets.Metric`
    metric.add_batch(all_predictions, all_targets)
```

注意：函数 `gather()` 要求所有的 tensor 具有相同的维度。比如：每个GPU上的数据在 padding 时，padding 的最大长度设置为当前这个 `mini_batch=16` 条数据中长度最大的那条数据的长度，就会导致多个GPU之间的 tensor 的维度不同，此时函数 `gather()` 不能正常工作。

## 运行分布式脚本

没有看

## 使用notebook运行

没有看

## 在TPU上训练

我哪有TPU

## 其他注意点说明

### 程序只在一个进程中执行

> 注：todo 这里需要看一下原文档中的 `process` 是否真的是平时所说的 "进程" 的意思？看源码确认一下；

在分布式训练的时候，以多GPU为例，我们的程序会同时运行在多张显卡上。那么比如打印日志、打印进度条等功能，只希望其执行一次就行了，否则如果有8张显卡，同一条日志打印8次看起来很不方便。

想要实现并发训练时程序只执行一次，只需将程序包到如下 `if` 判断内部即可：

```python
if accelerator.is_local_main_process:
    # Is executed once per server
```

其中标志 `accelerator.is_local_main_process` 就表示是否在主进程中。在这个 `if` 判断内部的代码，如果不是在主进程中，是不会执行的。

像打印进度条的 `tqdm` 库，可以按照如下方式使用：

```python
from tqdm.auto import tqdm

progress_bar = tqdm(range(args.max_train_steps), disable=not accelerator.is_local_main_process)
```

类似的，只有在主进程中才会打印进度条；

标志 `accelerator.is_local_main_process` 中的 `local` 是当前机器；当多机多GPU时，该标志在每台机器的主进程中都是True。在多机多GPU的情况下如果想要只在一台机器的主进程中执行，可以使用如下代码：

```python
if accelerator.is_main_process:
    # Is executed once only
```

最后，由于 `print` 函数使用比较频繁，每次包到 `if` 分支中比较麻烦，accelerator对其单独做了处理。直接使用 `accelerator.print` 即可实现在每台机器中只打印一次的功能。

### 等待所有进程完成，再继续执行

在进行分布式训练时，不可避免的会出现有的进程执行的快、有的进程执行的慢的情况。而有些时候我们希望每个进程都已经执行完了各自需要执行的内容之后，再进行后面的。可以使用如下代码实现该功能：

```python
accelerator.wait_for_everyone()
```

这行代码的作用为：先执行到这行代码的进程阻塞，一直等待到所有的进程都执行到了这行代码之后，再同时开始执行后面的代码；

如果是只有一个进程，那么上面这行代码什么都不做。

### 保存和加载模型



### Gradient clipping

如果之前在训练过程中使用了 gradient clipping，那么需要:

* 使用函数 `accelerator.clip_grad_norm_` 替换原来的 `torch.nn.utils.clip_grad_norm_`；

* 使用函数 `accelerator.clip_grad_value_` 替换原来的 `torch.nn.utils.clip_grad_value_`；

### 混合精度


### DeepSpeed

## 内部原理和机制
