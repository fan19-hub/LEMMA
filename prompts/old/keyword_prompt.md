Please generate keywords that can help verify the authenticity of the news mentioned in the text. The keywords should reflect the key aspects of the news that can be researched or verified.
I will give you one example:
**example input1**:
波士顿马拉松爆炸案的受害者实际上是尼克·沃格特，一名前美国陆军军官，2011年11月在阿富汗坎大哈失去了双腿，当时他是第1斯瑞克步兵师第25旅的一员。这里发生的事情比媒体要多!波士顿马拉松爆炸案演员再次被确认!这个人是一名在阿富汗失去双腿的美国士兵。直播视频可能是由摄像师安排拍摄的，所谓的炸弹只是烟雾弹，对人的伤害极其有限，几乎没有产生烟雾效果。

**explain**:
The first row should be True. This is not personal memory or perference
波士顿马拉松爆炸案 is the summary of the topic. 烟雾弹 is the key thing that the text wants to argue about. 尼克·沃格特 波士顿 are crucial names so you must include them
演员 美国军官 失去右腿 are things easily to be fake and need to verify 

**example_output1**:
True
尼克·沃格特 波士顿马拉松爆炸案  烟雾弹
演员 美国军官 失去右腿


**example input2**:
#塘沽爆炸真相##天津爆炸#怎么可能就50人遇难！对面就是居民楼！方圆三十公里都有人受伤！光是消防官兵救牺牲掉几百人！！政府怎么了、就这么腐败下去了吗？？其他国家报道都是几千人遇难、政府以为这样就能瞒得住群众吗？太让人心寒

**explain**:
The first row should be True. This is not personal memory or perference
塘沽爆炸 真相 is the summary of the topic. 遇难人数 is the key thing that the text wants to argue about. 塘沽 is the crucial name.
天津 塘沽 50人 are things easily to be fake and need to verify 

**example_output2**:
True
塘沽爆炸 真相 遇难人数
天津 塘沽 50人

**example input3**:
今天炖了鱼，味道非常鲜美。但是国足的比赛看的我很糟心，踢得太烂了

**explain**:
The first row should be False. Because 今天炖鱼 is a very personal memory and experience. And 踢得烂 鲜美 are very personal preferences that can not be verified objectively.

**example_output3**:
False
炖鱼 鲜美 国足 踢得烂
今天比赛



**rules**:
The number of keywords should be less than 5
Split the long keyword into smaller ones
Do not repeat words!
The ouput should include 3 rows.
Ignore the meaningless words like @Fan @中央电视台
Only give me keywords, do not explain


**template**:
First row: if you are sure the text can not be judged to be fake objectively (pure feelings, very personal memories), such as the taste of food and the difficulty of math, write "False" here. Otheraise, write "True" here.
Second row: summarize the topic and the key information points that the text wants to convey. Use no more than 3 keywords. If there are names (place or person) which are **crucial** to this statement, you must write it at the beginning of this row
Third row: Use points that are most likely to be fake and need to be verified to form no more than 3 keywords

Now, to judge if the **News input** is fake, what keywords should I give the search engine. You always need to follow the **rules**. The output should follow **template**. 
**News input**