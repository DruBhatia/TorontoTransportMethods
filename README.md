Python application capable of cleaning census data from Statistics Canada to produce a colour-coded map of
the fastest transport methods (walking, biking, transit, driving) to traverse the Greater Toronto Area from any origin
node.

Data for travel times was obtained using Google Maps API. Census data was cleaned and formatted into plots
using the <geopandas> and <matplotlib> Python libraries in the Anaconda environment.

Here are a few sample maps showing the fastest transport method from 3 origin nodes - UofT, Union Station, and Pearson Airport.
Sector colours represent the fastest method to reach the sector from the selected origin node. 
Green sectors correspond to walking;
Yellow sectors correspond to biking;
Blue sectors correspong to public transit;
Red sectors correspond to driving by car.

![uoft_core_coloured](https://github.com/user-attachments/assets/94b053b2-eddf-4325-b2aa-3edf00004062)
![union_greater_coloured](https://github.com/user-attachments/assets/d11ff39e-acad-4614-a56a-58fb6b80bf9b)
![union_core_coloured](https://github.com/user-attachments/assets/db8c8c8b-3f13-469f-b09e-6a4d1d555b4a)
![pearson_greater_coloured](https://github.com/user-attachments/assets/0223595c-a3d1-4a8f-8f29-96fd72542c07)
![pearson_core_coloured](https://github.com/user-attachments/assets/115701b7-9bd4-4922-bdd4-8e04952677cb)
![uoft_greater_coloured](https://github.com/user-attachments/assets/3900ec5a-f629-479a-88e6-bb70ad4a9977)
