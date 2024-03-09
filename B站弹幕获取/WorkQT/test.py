from pyecharts import options as opts
from pyecharts.charts import WordCloud, Page, Line
from wordcloud import WordCloud as WC
from pyecharts.globals import SymbolType

# 准备文本数据
text = "Hello world! This is a word cloud example."

# 生成词频
word_freq = WC().process_text(text)

# 将词频转换为(词, 频率)的二元组列表
word_freq_list = [(k, v) for k, v in word_freq.items()]

# 创建一个Page对象
page = Page()

# 创建词云图
wordcloud = (
    WordCloud()
    .add("", word_freq_list, word_size_range=[20, 100], shape=SymbolType.DIAMOND)
    .set_global_opts(title_opts=opts.TitleOpts(title="Word Cloud"))
)

# 创建折线图
line = (
    Line()
    .add_xaxis(['A', 'B', 'C', 'D', 'E'])
    .add_yaxis('Series', [1, 3, 2, 5, 4])
    .set_global_opts(title_opts=opts.TitleOpts(title="Line Chart"))
)

# 将词云图和折线图添加到Page中
page.add(wordcloud)
page.add(line)

# 生成HTML文件
page.render("wordcloud_line.html")