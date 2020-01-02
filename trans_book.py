#!/usr/bin/env python
# coding: utf-8

# In[1]:


from translate_word_in_sentence import translate, get_trans, word_unknown, add_trans_to_sentence
import re
from stardict import DictCsv
from difflib import SequenceMatcher 
import itertools
import string
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import bs4
import argparse



# In[6]:


def process_book(epub_filename, output_filename, word_judge, dict_filename, token_filename):
    with open(token_filename, 'r') as f:
        token=f.read()
    sdict=DictCsv(dict_filename)
    
    try:
        with open(word_judge['exclude_word_filename'], 'r') as f:
            exclude_word_list=f.read()
    except:
        exclude_word_list=""

    book = epub.read_epub(epub_filename)

    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            raw_text=item.get_body_content().decode('utf-8')
            soup = BeautifulSoup(raw_text, 'lxml')
            for p in soup.find_all("p"):
                for idx, s in enumerate( p.contents):
                    if type(s)==bs4.element.NavigableString:
                        try:
                            s_t, w_t=add_trans_to_sentence(s, sdict, token, word_judge, exclude_word_list)
                            p.contents[idx].replace_with(s_t);
                        except:
                            pass
            item.content=str(soup.body).replace("<body>","").replace("</body>","") #非常难看但有效
    epub.write_epub(output_filename, book)


# In[ ]:


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Process subtitle.')
    parser.add_argument('-i', '--input', dest="input_filename", help="需要处理的epub电子书")
    parser.add_argument('-o', '--output', dest="output_filename", help='输出文件名')
    parser.add_argument('-include', nargs='?', dest="include_tag", type=str,
                        help='生词的定义: 包含哪些标记, 用空格隔开, 例如 cet6 toelf gre ielts',
                       default="cet6 gre ielts")
    parser.add_argument('-exclude', nargs='?', dest='exclude_tag', type=str,
                        help='生词的定义: 除外哪些标记, 用空格隔开, 例如 zk gk cet4',
                       default="zk gk cet4")
    parser.add_argument('-collins', nargs='?',dest='collins_threshold', type=int, 
                        help='collins星级', default=2)
    parser.add_argument('-bnc', nargs='?', dest='bnc_threshold', type=int,
                       help='英国国家语料库词频顺序bnc, 越大越难', default=5000)
    parser.add_argument('-frq', nargs='?', dest='frq_threshold', type=int,
                       help='当代语料库词频顺序frq, 越大越难', default=5000)
    parser.add_argument('-e', '--exclude_word', nargs='?', dest='exclude_word_filename', 
                        type=str, help='需要排除的单词列表, txt文件, 每行一个单词', 
                        default="exclude_word_list.txt")
    parser.add_argument('-l', '--word_length', nargs='?', dest='word_length', 
                        type=int, help='一定长度以上的单词将默认提示', 
                        default=10)

    
    args = parser.parse_args()
    word_judge={}
    word_judge["include_tag"]=args.include_tag 
    word_judge["exclude_tag"]=args.exclude_tag 
    word_judge["collins_threshold"]=args.collins_threshold 
    word_judge["bnc_threshold"]=args.bnc_threshold 
    word_judge['frq_threshold']=args.frq_threshold 
    word_judge['exclude_word_filename']=args.exclude_word_filename
    word_judge['word_length']=args.word_length
    
    process_book(args.input_filename, 
                 args.output_filename, 
                 word_judge,
                dict_filename="ecdict.csv", 
                token_filename='token.txt'
               )

