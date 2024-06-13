# %%
pip install fastai
# %%
pip install openpyxl

# %%
from fastai.tabular.all import *
from fastai.collab import *
from sklearn.metrics import mean_absolute_error, mean_squared_error

# %%
# 设置设备，优先使用 MPS，其次 CUDA，最后 CPU
device = torch.device('mps') if torch.backends.mps.is_available() else (
    torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
)
print(f"使用的设备: {device}")

# %%
# Load the data
data_df = pd.read_excel('transformed_jester_data.xlsx')
  

# %%
data_df.head()

# %%
# Load the jokes
jokes_df = pd.read_excel('Dataset4JokeSet.xlsx')

# %%
# 正文列增加列名joke
jokes_df.columns = ['joke']

# %%
#将jokes_df中的索引定义为joke_id
jokes_df = jokes_df.rename_axis('joke_id').reset_index()

# %%
#完成实验步骤中对数据集操作后执行
jokes_df.head()

# %%
data_df = data_df.merge(jokes_df)

# %%
ratings=data_df

# %%
split_timestamp = ratings['user_id'].quantile(0.8)  
train_ratings = ratings[ratings['user_id'] <= split_timestamp]
test_ratings = ratings[ratings['user_id'] > split_timestamp]

# %%
dls =CollabDataLoaders.from_df(train_ratings,item_name='joke',bs=64,device=device)

# %%
learn = collab_learner(dls,n_factors=50,y_range=(0,5.5))
learn.model.to(device)  
learn.dls.device = device 

# %%
# 添加早停和保存最佳模型的回调
callbacks = [
    EarlyStoppingCallback(monitor='valid_loss', patience=3),
    SaveModelCallback(monitor='valid_loss', fname='best_model')
]

# %%
learn.fit_one_cycle(100,5e-3,wd=0.1,cbs=callbacks)

# %%
# 在测试集上预测
test_dl = learn.dls.test_dl(test_ratings)
preds, _ = learn.get_preds(dl=test_dl)

# %%
# 计算RMSE和MAE
rmse = np.sqrt(mean_squared_error(test_ratings['rating'], preds))
mae = mean_absolute_error(test_ratings['rating'], preds)

# %%
print("测试集 RMSE: ", rmse)
print("测试集 MAE: ", mae)

# %%
# 为新用户选择一个未使用的user_id
new_user_id = ratings['user_id'].max() + 1

# %%
# 添加新用户的评分数据
new_ratings_df = pd.DataFrame({
    'user_id': [new_user_id, new_user_id,new_user_id],
        'joke_id': [107,149,34],
        'rating': [10,9,2],
    })
ratings = pd.concat([ratings, new_ratings_df])

# %%
# 创建新的数据加载器
dls = CollabDataLoaders.from_df(train_ratings,item_name='joke',bs=64,device=device)

# %%
# 重新训练模型
learn = collab_learner(dls,n_factors=50,y_range=(0,5.5))
learn.model.to(device)  # 将模型移动到指定设备
learn.dls.device = device  # 将数据加载器的设备设为指定设备

# %%
# 添加早停和保存最佳模型的回调
callbacks = [
    EarlyStoppingCallback(monitor='valid_loss', patience=3),
    SaveModelCallback(monitor='valid_loss', fname='best_model')
]

# %%
learn.fit_one_cycle(100,5e-3,wd=0.1,cbs=callbacks)

# %%
joke_ids = ratings['joke_id'].unique()  
joke_ids_new_user = ratings.loc[ratings['user_id'] == new_user_id, 'joke_id']  
joke_ids_to_pred = np.setdiff1d(joke_ids, joke_ids_new_user) 

# %%
testset_new_user = pd.DataFrame({
    'user_id': [new_user_id] * len(joke_ids_to_pred),
    'joke_id': joke_ids_to_pred,
    'joke':jokes_df.loc[jokes_df['joke_id'].isin(joke_ids_to_pred),'joke']
})


# %%
test_dl = learn.dls.test_dl(testset_new_user)
preds, _ = learn.get_preds(dl=test_dl)

# %%
# 将预测结果添加到testset_new_user DataFrame中
testset_new_user['rating'] = preds.numpy()

# %%
# 获取评分最高的前10部笑话
top_10_jokes = testset_new_user.nlargest(10, 'rating')

# %%
print("新用户的前10部笑话推荐：")
print(top_10_jokes[['joke','rating']])

# %%


# %%


# %%



