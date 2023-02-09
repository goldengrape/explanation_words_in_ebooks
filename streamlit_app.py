import streamlit as st
from trans_book import process_book
import os 
from io import BytesIO, StringIO

# parser.add_argument('-i', '--input', dest="input_filename", help="需要处理的epub电子书")
# parser.add_argument('-o', '--output', dest="output_filename", help='输出文件名')
# parser.add_argument('-include', nargs='?', dest="include_tag", type=str,
#                     help='生词的定义: 包含哪些标记, 用空格隔开, 例如 cet6 toelf gre ielts',
#                     default="cet6 gre ielts")
# parser.add_argument('-exclude', nargs='?', dest='exclude_tag', type=str,
#                     help='生词的定义: 除外哪些标记, 用空格隔开, 例如 zk gk cet4',
#                     default="zk gk cet4")
# parser.add_argument('-collins', nargs='?',dest='collins_threshold', type=int, 
#                     help='collins星级', default=2)
# parser.add_argument('-bnc', nargs='?', dest='bnc_threshold', type=int,
#                     help='英国国家语料库词频顺序bnc, 越大越难', default=5000)
# parser.add_argument('-frq', nargs='?', dest='frq_threshold', type=int,
#                     help='当代语料库词频顺序frq, 越大越难', default=5000)
# parser.add_argument('-e', '--exclude_word', nargs='?', dest='exclude_word_filename', 
#                     type=str, help='需要排除的单词列表, txt文件, 每行一个单词', 
#                     default="exclude_word_list.txt")
# parser.add_argument('-l', '--word_length', nargs='?', dest='word_length', 
#                     type=int, help='一定长度以上的单词将默认提示', 
#                     default=10)


# args = parser.parse_args()
# word_judge={}
# word_judge["include_tag"]=args.include_tag 
# word_judge["exclude_tag"]=args.exclude_tag 
# word_judge["collins_threshold"]=args.collins_threshold 
# word_judge["bnc_threshold"]=args.bnc_threshold 
# word_judge['frq_threshold']=args.frq_threshold 
# word_judge['exclude_word_filename']=args.exclude_word_filename
# word_judge['word_length']=args.word_length

# process_book(args.input_filename, 
#                 args.output_filename, 
#                 word_judge,
#             dict_filename="ecdict.csv", 
#             token_filename='token.txt'
#             )

# st.title('英语电子书生词翻译')
# st.write('''# 上传电子书''')

uploaded_file = st.file_uploader("选择电子书文件", type=["epub"])
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    # 建立临时tmp文件夹
    if not os.path.exists('tmp'):
        os.mkdir('tmp')
    # 保存上传的文件
    epub_filename=uploaded_file.name
    epub_filename_with_path=os.path.join('tmp', epub_filename)
    with open(epub_filename_with_path, 'wb') as f:
        f.write(bytes_data)
    # 生成输出文件名
    output_filename="output"+uploaded_file.name
    output_filename_with_path=os.path.join('tmp', output_filename)
# include_tag
# 多选cet6 toelf gre ielts zk gk cet4
include_tag = st.multiselect(
    'Include Tag',
    ['cet6', 'toelf', 'gre', 'ielts', 'zk', 'gk', 'cet4'],
)

# exclude_tag
# 多选cet6 toelf gre ielts zk gk cet4
exclude_tag = st.multiselect(
    'Exclude Tag',
    ['cet6', 'toelf', 'gre', 'ielts', 'zk', 'gk', 'cet4'],
)
# -include 应当包含的标签, 用空格隔开, 例如cet6 toelf gre ielts
# -exclude 应当除外的标签, 例如zk gk (中考 高考)
# -collins collins星级, 越小越难
# -bnc 英国国家语料库词频顺序bnc, 越大越难
# -frq 当代语料库词频顺序frq, 越大越难

# collins collins
# select slider
collins_threshold=st.select_slider(
    'Collins',
    options=[1, 2, 3, 4, 5],
    value=2
)
# bnc
# 整数slider
bnc_threshold=st.slider(
    'BNC',
    min_value=1000,
    max_value=10000,
    value=5000,
    step=100
)
# frq
# 整数slider
frq_threshold=st.slider(
    'FRQ',
    min_value=1000,
    max_value=10000,
    value=5000,
    step=100
)
word_length=10

word_judge={}
word_judge["include_tag"]=" ".join(include_tag)
word_judge["exclude_tag"]=" ".join(exclude_tag)
word_judge["collins_threshold"]=collins_threshold 
word_judge["bnc_threshold"]=bnc_threshold 
word_judge['frq_threshold']=frq_threshold 
word_judge['exclude_word_filename']='exclude_word_list.txt'
word_judge['word_length']=word_length

# token
token = st.text_input(
            "Token", type="password", key="password"
        )

button = st.button('开始处理')

if button:
    if token == "":
        st.write("请填写token")
    else:
        process_book(epub_filename_with_path, 
                    output_filename_with_path,
                    word_judge,
                dict_filename="ecdict.csv", 
                token=token
                )

    

