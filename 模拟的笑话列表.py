import streamlit as st  
import random
# 模拟的笑话列表  
jokes = [  
    "为什么电脑永远不会感冒？因为它有Windows（窗口）！",  
    "程序员最讨厌的两件事：一是别人修改他的代码，二是别人不修改他的代码。",  
    "如果你认为教育很贵，那么请试试无知的价格吧！"  
]  
  
# 初始化用户评分字典（用于存储用户对笑话的评分）  
user_ratings = {}  
  
# 模拟的推荐笑话函数（这里仅返回初始笑话列表的随机子集）  
def recommend_jokes(num_jokes):  
    return random.sample(jokes, num_jokes)  
  
# 计算用户满意度（这里仅基于随机值进行模拟）  
def calculate_satisfaction(ratings):  
    # 假设满意度是基于评分的平均值，但这里我们为了示例随机返回一个值  
    return random.random() * 5  # 返回0到5之间的随机满意度值  
  
# 主应用程序逻辑  
def main():  
    st.title("笑话评分与推荐")  
  
    # 初始显示3个笑话并允许用户评分  
    for i, joke in enumerate(random.sample(jokes, 3), 1):  
        st.subheader(f"笑话 {i}")  
        st.write(joke)  
        rating = st.slider("请为该笑话打分（1-5）", 1, 5, 1)  
        user_ratings[joke] = rating  
  
    # 显示推荐的笑话并允许用户评分  
    recommended_jokes = recommend_jokes(5)  
    st.subheader("为您推荐的笑话：")  
    for joke in recommended_jokes:  
        st.write(joke)  
        rating = st.slider("请为该推荐的笑话打分（1-5）", 1, 5, 1)  
        if rating is not None:  # 确保slider有值（可能用户没有评分）  
            user_ratings[joke] = rating  
  
    # 计算并显示用户满意度  
    satisfaction = calculate_satisfaction(user_ratings.values())  
    st.subheader("用户满意度：")  
    st.write(f"基于您的评分，本次推荐的满意度为 {satisfaction:.2f}（满分5分）。")  
  
if __name__ == "__main__":  
    main()