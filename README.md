# Leukemia-Treatment-Application

## Pre-requisites

- Python >= 3.6.1
- Matlab >= R2022b
  - Statistics and Machine Learning Toolbox Add-on
  - Symbolic Math Toolbox
  - Simulink

## 1.0 Setup

```
git clone https://github.com/liu-allan/Leukemia-Treatment-Application.git
cd <path/to/Leukemia-Treatment-Application>
pip install --upgrade pip
pip install -r requirements.txt
git submodule update --init --recursive
```

## 1.1 Setup on MacOS M1 

- To run matlabengine on MacOS M1, need to install Rosetta2 on the machine. 
- To check whether the terminal is Rosetta2 enabled
  ```
  uname -m
  ```
  - if it returns x86_64, then it means you are on a Rosetta2 enabled terminal
  - if it returns arm64, then it means it is not enabled

- To install Rosetta2, open Terminal and run this command:
  ```
  softwareupdate --install-rosetta --agree-to-license
  ```
- After installing Rosetta2, please follow this youtube link: https://www.youtube.com/watch?v=9W8rTTE1WEA
  - Go to Finder -> Applications -> Utilities -> Terminal
  - Right click on the Terminal app and select "Duplicate" and rename the duplicate app to something else
  - Then right click on the duplicated Terminal and select "Get Info" and checkmark "Open using Rosetta"

- Now you can run the first command again to check whether you are running on x86_64

- Download miniconda3 x86_64 bash installer using this link: https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
- Follow step 4 and onwards to download miniconda3: https://towardsdatascience.com/how-to-install-miniconda-x86-64-apple-m1-side-by-side-on-mac-book-m1-a476936bfaf0

- After success installation of miniconda3 x86_64, to run the entire project:
  - Open Rosetta2 enabled terminal
  - Set up virtual environment using the following command:
  ```
  /usr/bin/python3 -m venv env
  source env/bin/activate 
  ```
  - Then continue to follow the 1.0 Setup.

## 1.2 Command when submodule is updated
- When the Leukemia Treatment Project is updated, need to use the following command to make sure that the repo contains the newest update from the submodule.
  ```
  git submodule update --recursive
  ```
 
## 2.0 How to use

Open the application in the root directory of the repository.
```
python app.py
```
### 2.1 Login Page
Login with credentials. To create a new user, see [section 5.0](https://github.com/liu-allan/Leukemia-Treatment-Application/tree/documentation#40-optional-create-a-new-user)

There are two existing example oncologists profiles in the database. The account usernames and passwords are the following:
- Username: allan, Password: wordpass
- Username: angus, Password: password

![Login Page](https://user-images.githubusercontent.com/44624612/231532389-985b40ae-3497-4cc1-8cf8-b46936e97597.png)

After logging in, log out at any time by pressing the `Log Off` button in the top right of the application. 

### 2.2 Patient List Page

1. To create a patient profile, click on the plus icon in the top left.
2. To search for an existing patient, type the patient's name into the search bar
    1. Press Advanced search button to toggle between default and advanced search. Advanced search allows the user to search patients by name and ID. Only patients that satisfy both the name and ID entered will be displayed.
3. To select an existing patient, click on the patient's tile.
4. To delete an existing patient, press the delete button inside the patient's list item.

![Patient List Page](https://user-images.githubusercontent.com/44624612/231534114-3fa2d8e7-ed4e-4fb9-8d4f-28473c73a298.png)

### 2.3 Patient Form Page

- Fill in patient parameters 
- Press Save to add the new patient to the list
- Press Cancel to return to the previous page

![Patient Form Page](https://user-images.githubusercontent.com/44624612/231534394-62da01d8-dfd0-48ec-a9c6-9082e1b726ce.png)

### 2.4 Patient Information Page

- Press Edit to change patient parameters.
- If there is new data, input the prescribed dosage, ANC measurement and date of measurement.
- Press Save to save the record into the database.
- Input the number of cycles into the future to run (Note: no negative numbers or numbers > 99 as the calculate button will be disabled) (if '1' is inputted, there will actually be 2 cycles ran)
- Press Calculate to run the model with the newest and previously saved records. 

![Patient Information Page](https://user-images.githubusercontent.com/44624612/231534625-c6de4f25-946d-4278-98df-4cd431252e2e.png)

Navigate to other pages by pressing the icons on the left. If the model has already been run for the patient, the user can return to the dashboard without running the model again by pressing the Dashboard icon on the left. 

![tab legend](https://user-images.githubusercontent.com/44624435/230222852-0e2b3d38-e36b-417c-b5ba-2b42753016fa.png)

Note: The model only takes the most recent dosage and ANC measurement into consideration. The code needs to be modified in order to run the entire patient's history.


### 2.5 Dashboard

The model can take a few minutes (4-5 minutes per cycle) to complete. This is normal. The dashboard page will be shown as below when performing calculation. When performing calculation, all other buttons are disabled to prevent multiple calculation happening simultaneously. 

![Loading Page](https://user-images.githubusercontent.com/44624612/231534968-4b815a1b-865f-40bb-a9c3-83cf943a0eaa.png)

After calculation, the dashboard page will show two main components.
1. The top part is the ANC trajectories for two strategies. 
2. The bottom part is the dosage tables for two strategies.

![Dashboard Page](https://user-images.githubusercontent.com/44624612/231587587-8ac735a0-17ca-4ce1-bbc0-e6165d7022c6.png)

- Navigate to previous pages using the tabs on the left.
- Press and hold left click to pan the graph.
- Press and hold right click to stretch the axes (place the cursor on the axes when you do this).
- Use the scroll wheel on the graph to zoom in and out.

## 3.0 Matlab Model

The Matlab Model is called through `runModel()` found in `matlab_script.py`. It calls `runController.m` found in the [`/Leukemia-Treatment-Project`](https://github.com/liu-allan/Leukemia-Treatment-Project/tree/d8ab68d451eea82b5519327db5ec79ee9549ffa2) directory

## 4.0 Database

To view tables on vscode, install https://marketplace.visualstudio.com/items?itemName=alexcvzz.vscode-sqlite

### 4.1 Patients

| id | user_id | name |phone_number|birthday|age|blood_type|all_type|weight|height|body_surface_area|oncologist_id|sex| 
|:--:|:-------:|:----:|:----------:|:------:|:-:|:--------:|:------:|:----:|:-----|:---------------:|:-----------:|:-:|
|int|string|string|string|string (yyyyMMdd)|string|string|string|string|string|string|string|string|

The Patients Table is encrypted with the plaintext password as the key.

### 4.2 Measurements

|time|anc_measurement|dosage_measurement|patient_id|
|:--:|:-------------:|:----------------:|:--------:|
|string (yyyyMMdd)|float|float|int|

### 4.3 Oncologists

|username|password|full_name|is_admin|
|:------:|:------:|:-------:|:------:|
|string (yyyyMMdd)|float|float|bool|

To get a better understanding of the tables, one can look at the schemas in [`database.py`](https://github.com/liu-allan/Leukemia-Treatment-Application/blob/main/database.py)

## 5.0 Optional: Create a new user

To create a new user, login with credentials: username: admin, password: admin

Then click on the plus icon in the top left.

![Oncologist List Page](https://user-images.githubusercontent.com/44624612/231537908-f74c2d53-4287-4c5c-b141-e8334a6decbe.png)

Fill out the form and press save to complete registration.

![Oncologist Form Page](https://user-images.githubusercontent.com/44624612/231538052-befdcb2c-4cd9-4a63-8279-a2ba7d2889f0.png)

Logout from the admin account and login with the newly created account.


