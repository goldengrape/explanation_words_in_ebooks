#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import re
# from stardict import DictCsv
from difflib import SequenceMatcher 
import itertools
import string


# In[1]:


def translate(source, token):

    import requests
    import json
    
    url = "http://api.interpreter.caiyunai.com/v1/translator"
    
    #WARNING, this token is a test token for new developers, and it should be replaced by your token
#     token = "3975l6lr5pcbvidl6jl2"
    
    
    payload = {
            "source" : source, 
            "trans_type" : "en2zh",
            "request_id" : "demo",
            "detect": True,
            }
    
    headers = {
            'content-type': "application/json",
            'x-authorization': "token " + token,
    }
    
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

    return json.loads(response.text)['target']
def longestSubstring(str1,str2): 
     # 两个字符串最长公共字符串
     # initialize SequenceMatcher object with  
     # input string 
    seqMatch = SequenceMatcher(None,str1,str2) 
  
     # find match of longest sub-string 
     # output will be like Match(a=0, b=0, size=5) 
    match = seqMatch.find_longest_match(0, len(str1), 0, len(str2)) 
  
     # print longest substring 
    if (match.size!=0): 
          return (str1[match.a: match.a + match.size])  
    else: 
          return ""
def get_trans(word_trans_from_dict, word_trans_from_translator, sentence_trans):
    # 句子中的单词含义, 如果没有公共的, 就返回查到的词
    match=longestSubstring(sentence_trans,word_trans_from_dict)
    match=re.sub('[a-zA-Z0-9.\n ]*',"",match) #只留下中文
    exclude_list=["要","着","了","过","来","的","是","说","去","到","给","做","有","看","操"]
    if any(match == e for e in exclude_list):
        match=""
    if match=="":
        return re.sub('[a-zA-Z0-9.\n ]*',"",word_trans_from_translator)
    else:
        return match
def word_unknown(word_query, word_judge,exclude_word_list):
    if not(word_query):
        return False #查不到就算了
    # check in exclude_word_list
    if word_query['word'] in exclude_word_list:
        return False
    
    # 是否认识?
    include_tag=word_judge["include_tag"] 
    exclude_tag=word_judge["exclude_tag"]


    collins_threshold=word_judge["collins_threshold"]; collins_default=True
    bnc_threshold=word_judge["bnc_threshold"]; bnc_default=True
    frq_threshold=word_judge["frq_threshold"]; frq_default=True
    
    # check tag
    include_list=include_tag.lower().split()
    exclude_list=exclude_tag.lower().split()
    if word_query['tag']: # 如果该单词有tag标记
        word_tag=word_query['tag'] 
        tag_chk=(not(any(e in word_tag for e in exclude_list)) 
                 and 
                 any(i in word_tag for i in include_list))    
    else:
        tag_chk=True  #如果该单词没有tag标记, 默认为
    
    # check collins
    collins_chk = (word_query['collins']<=collins_threshold) if word_query['collins']>=0 else collins_default
    
    # check bnc
    bnc_chk=(word_query['bnc']>=bnc_threshold) if word_query['bnc']>0 else bnc_default
    
    # check frq
    frq_chk=(word_query['frq']>=frq_threshold) if word_query['bnc']>0 else frq_default
    
    # check word length
    length_chk=len(word_query['word']) >= word_judge['word_length']
    

    return ((tag_chk+collins_chk+bnc_chk+frq_chk) >=3 or length_chk)
def add_trans_to_sentence(s, sdict, token, word_judge, exclude_word_list, filter_word=True):
    sentence=s.replace("\\N", " ").replace("\n", " ").replace("."," ").replace(",", " ")
    words=sentence.split()
    words_to_trans={}
    for word in words:
        word_query=sdict.query(word) if sdict.query(word) else sdict.query('unknown')   
        if filter_word:
            if word_unknown(word_query,word_judge,exclude_word_list):
                words_to_trans[word]=word_query['translation']
        else:
            words_to_trans[word]=word_query['translation']
    if words_to_trans: # if words_to_trans is not empty
        to_trans_list=[[sentence], words_to_trans.keys()]
        to_trans_list=list(itertools.chain(*to_trans_list))
        trans=translate(to_trans_list,token)
        sentence_trans=trans[0]
        word_with_trans={}
        for idx, word in enumerate(words_to_trans.keys()):
            word_trans=trans[idx+1]
            word_with_trans[word]=get_trans(words_to_trans[word], word_trans, sentence_trans)
        for (word, meaning) in word_with_trans.items():
            meaning=word+"("+meaning+")"
            s=s[0:s.find(word)]+meaning+s[(s.find(word)+len(word)):]
    return s, list(words_to_trans.keys())


# In[ ]:




