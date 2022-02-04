# Accelerate

## 特征

* 提供混合精度、分布式训练（单多GPU、多机多GPU、TPU等等）等功能，在原训练代码的基础上只需要修改少量代码；

* 提供命令行工具可以快速测试本地环境

## 用法简单，代码修改量少

传统的使用pytorch的训练代码一般如下：

```python
my_model.to(device)

for batch in my_training_dataloader:
    my_optimizer.zero_grad()
    inputs, targets = batch
    inputs = inputs.to(device)
    targets = targets.to(device)
    outputs = my_model(inputs)
    loss = my_loss_function(outputs, targets)
    loss.backward()
    my_optimizer.step()
```

如果要使用accelerate只需做如下代码的修改就可以轻松运行到分布式环境下：


<div>
<pre>
<code class="language-python hljs">
<font color=green>+ from accelerate import Accelerator</font>
<span></span>
<font color=green>+ accelerator = Accelerator()</font>
<font>  # Use the device given by the `accelerator` object.</font>
<font color=green>+ device = accelerator.device</font>
<font>  my_model.to(device)</font>
<font>  # Pass every important object (model, optimizer, dataloader) to `accelerator.prepare`</font>
<font color=green>+ my_model, my_optimizer, my_training_dataloader = accelerate.prepare(</font>
<font color=green>+     my_model, my_optimizer, my_training_dataloader</font>
<font color=green>+ )</font>
<span></span>
<span>  for batch in my_training_dataloader:</span>
<font>      my_optimizer.zero_grad()</font>
<font>      inputs, targets = batch</font>
<font>      inputs = inputs.to(device)</font>
<font>      targets = targets.to(device)</font>
<font>      outputs = my_model(inputs)</font>
<font>      loss = my_loss_function(outputs, targets)</font>
<font>      # Just a small change for the backward instruction</font>
<font color=red>-     loss.backward()</font>
<font color=green>+     accelerate.backward(loss)</font>
<font>      my_optimizer.step()</font>
</code>
</pre>
</div>


上述方式还需要自己通过函数 `to(device)` 指定设备，更推荐的用法是由 Accelerator 自动管理设备信息，代码如下：

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

## 支持的环境

* CPU

* 单GPU

* 多GPU单节点

* 多GPU多节点

* TPU

* FP16 with native AMP

* DeepSpeed

## 目录

#### Get Started

* [Quick tour](./quick_tour.md)
    * 主要用法
    * 分布式评估
    * 运行分布式脚本
    * 使用notebook运行
    * 在TPU上训练
    * 其他注意点说明
    * 内部原理和机制
* [Installation](./Installation.md)

#### API Reference

* [Accelerate](./accelerator.md)
* [Notebook Launcher](./notebook_launcher.md)
* [Kwargs Handlers](./kwargs_handlers.md)
* [Internals](./internals.md)
