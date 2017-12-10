from wordcloud import WordCloud
import jieba
import matplotlib.pyplot as plt


def draw_wordcloud():
    #读入一个txt文件
    comment_text = open('/Users/admin/Desktop/spider/spider/jd_comment/comment.txt','r').read()
    #结巴分词，生成字符串，如果不通过分词，无法直接生成正确的中文词云
    cut_text = " ".join(jieba.cut(comment_text))
    d = path.dirname(__file__) # 当前文件文件夹所在目录
    cloud = WordCloud(
        #设置字体，不指定就会出现乱码
        font_path="Songti.ttf",
        #font_path=path.join(d,'simsun.ttc'),
        #设置背景色
        background_color='white',
        #允许最大词汇
        max_words=2000,
        #最大号字体
        max_font_size=40
    )
    word_cloud = cloud.generate(cut_text) # 产生词云
    word_cloud.to_file("cloud.jpg") #保存图片
    #  显示词云图片
    # plt.imshow(word_cloud, interpolation='bilinear')
    # plt.axis('off')
    # plt.show()


if __name__ == '__main__':

    draw_wordcloud()
