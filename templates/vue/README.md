# Vue 3 + Typescript + Vite

### 动画时间在素材时间变化的时候没有变化（未开始代码编写）前提条件：动画的startTime和duration是相对于素材的，startTime默认为0，duration默认为素材duration
```
①.动画的startTime==0，动画duration===素材的duration，则动画startTime=0,动画duration跟随素材duration变化
②.动画的startTime=0,动画duration<素材的duration，则不动
③.动画startTime>0,动画startTime+duration<素材的duration，则不动
④.动画startTime>0，动画startTime+duration==素材的duration，则动画duration不动，startTime跟随素材的duration变化而变化（类似出场动画）

PS：②会随着素材的duration变化变成④，④ 变化后也许会随着素材的duration变化而变成①，之后随着①的规则变化
```


### 重置样式、加入素材的素材大小算法
```
1.如果素材宽高<= w和h，用素材宽高
2.如果素材宽高至少一边>w||h ,则等比缩放，contain画布
```

### 场景增减时间的时候素材时间变化算法
```
前提条件：素材的startTime、endtime、duration是相对于场景的，startTime默认为0，duration和endtime默认为场景duration，以下规则参考来画
①.素材的endTime==场景的duration,则素材的startTime，不变，endTime跟随场景的duration变化
②.素材的endTime < 场景的duration，则素材不变化
PS：
1.场景时间最少只能缩短成1秒，当①变化的素材startTime==endtime的时候，场景时间缩短，素材startTime和endtime跟随场景的duration变化，如果这时候场景时间增加，按①执行
2.随着场景时间缩短，②会变成①
```

### 不同宽高比的素材替换的时候的宽高变化规则：
```
①.old素材宽高和new素材宽高都小于场景宽高的情况下，new素材的短边长度 等于 old素材的短边长度，长边自适应，可以保证来回替换的时候素材的宽高不变
②. 按①计算出来new素材宽高有一边大于场景宽高的情况下：
   old素材的矩形方向（竖/横）和new素材相同的情况下，不动（风险点：如果替换成宽高差别很大的矩形素材，会出现超出编辑区域很多的情况）；
   old素材的矩形方向（竖/横）和new素材不同的情况下，new素材的长边最大为场景对应边的2倍。（风险点：来回替换会使素材缩小）
```


### 比例切换
```
参考云剪辑：
1.位置的x、y分别按照场景宽度、高度变化按比例以元素中心点定位
2.width和height 全都按照场景高度的变化按比例变化
```