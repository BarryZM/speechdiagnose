### questions order in dictionary
questions will be asked in the order of the dictionary of question  
in some case, some questions are detailed inquiries of former question, e.g.  
'出血反复吗？', '出血量多吗？' are detailed inquiries of '牙龈出血吗？'  
make sure the detailed inquiries are listing after the main question, like:
```
{
'牙龈出血吗？',
'出血反复吗？',
'出血量多吗？',
}
```
And the possible corresponding features are set up as  
for
```
['牙龈出血', '出血反复', '出血量多']  
```
are
```
[0, 0, 0]
[0, 1, 0]
[0, 0, 1]
[0, 1, 1]
[1, 1, 1]
```
Notice that when main qusetion get a negative feture '1', there will be only one situation for the features of detailed inquiries. That means when if main question get a negative answer, the detailed inquiries will not be asked.


### 回答和提问中的描述都可以对应同一个的特征值目录
例如：
'我头疼'
和
询问'请问你有头疼吗?'， 回答'疼'
都会指向诊断第250维特征值为0
但是回答可能会省略主语（病症部位）
如何使得省略主语的回答描述对应到正确的特征编码

### 思必驰NLU返回json response语义槽顺序问题
思必驰NLU返回json response语义槽顺序是按照哈希表排序的，因此无法得到用户回答中语义槽的顺序

### 证候输入
各项证候描述以断行分开
每一项证候描述分客体与描述，中间以空格分开
如何区分客体与描述（界定空格位置）？
一般而言，对症状的提问
当回答可以以
'客体+描述'' 或单单 '描述''
来回答时，需明确分开客体与描述

例如：
'请问您咳嗽频繁吗？'
回答可以是
'咳嗽频繁'或'频繁'
因此在输入'咳嗽频繁'这一证候描述时需以空格分开客体与描述，即'咳嗽 频繁'

特别是描述的意义是与上下文有依赖关系的时候，例如上述例子中
当'频繁'作为'请问您咳嗽频繁吗？'的回答指向特征'咳嗽频繁'
当'频繁'作为'请问您头痛频繁吗？'的回答则指向特征'头痛频繁'
描述是否可以和其他客体组合指向不同的特征是界定客体与描述的一个标准

由上可得，当确定描述不依赖上下文是，可将整个证候描述作为描述，在前面加空格
例如：'头晕'，晕只能表示头晕，故'头晕'可作为描述，即输入为' 头晕'