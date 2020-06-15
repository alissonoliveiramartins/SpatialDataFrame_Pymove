#!/usr/bin/env python
# coding: utf-8

# In[1]:


import folium


# In[2]:


from pymove import SpatialDataFrame


# In[3]:


pontos = { 'lat': [-38.620930,-38.594566,-38.620953, -38.461146, -38.460760, -38.622756, -38.622822, -38.622792, -38.622860, -38.622918 ],
    'lon': [-5.885045, -5.866674, -5.885136, -6.048506, -6.048777, -5.886606, -5.886132, -5.886149, -5.886479, -5.886527]}


# In[4]:


spatial = SpatialDataFrame(pontos)


# In[5]:


spatial.head()


# In[6]:


mapa_jaguaribe1 = folium.Map([-5.88279,-38.6311735], zoom_start=15)
locs = zip(spatial.lon, spatial.lat)

for location in locs:
    folium.Marker(location=location, ).add_to(mapa_jaguaribe1)
mapa_jaguaribe1


# In[7]:


spatial.len()


# In[8]:


spatial.max()


# In[9]:


spatial.count()


# In[10]:


dic = spatial.to_dict()


# In[11]:


dic


# In[12]:


spatial.to_numpy()


# In[13]:


type(spatial)


# In[14]:


spatial.lat


# In[15]:


spatial.lng


# In[16]:


spatial.loc()


# In[17]:


spatial.iloc()


# In[18]:


spatial.unique


# In[19]:


spatial.head()


# In[20]:


spatial.plot_all_features()


# In[21]:


spatial.count()


# In[22]:


spatial.plot()


# In[23]:


type(spatial)


# In[24]:


spatial.loc()


# In[25]:


spatial.values


# In[26]:


from pandas import DataFrame


# In[43]:


spatial1= SpatialDataFrame(DataFrame(pontos), latitude="lat", longitude="lon", type_='dask')


# In[44]:


spatial1.head()


# In[50]:


spatial1.shape()


# In[51]:


spatial1.lng()


# In[52]:


type(spatial1)


# In[56]:


spatial1.lat()


# In[ ]:




