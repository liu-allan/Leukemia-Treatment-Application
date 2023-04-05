# Leukemia-Treatment-Application

## Pre-requisites

- Python >= 3.6.1
- Matlab >= R2022b
  - Statistics and Machine Learning Toolbox Add-on

## 1.0 Setup

```
git clone https://github.com/liu-allan/Leukemia-Treatment-Application.git
cd <path/to/Leukemia-Treatment-Application>
pip install --upgrade pip
pip install -r requirements.txt
```

## 2.0 How to use

Open the application in the root directory of the repository.
```
python app.py
```
Login with credentials. To create a new user, see [section 4.0](https://github.com/liu-allan/Leukemia-Treatment-Application/tree/documentation#40-optional-create-a-new-user)

![image](https://user-images.githubusercontent.com/44624435/226797287-7ec91a25-df3c-48b4-99d3-2bb32287f7fa.png)

After logging in, log out at any time by pressing the `Log Off` button in the top right of the application. 


### 2.1 Patient List Page

1. To create a patient profile, click on the plus icon in the top left.
2. To search for an existing patient, type into the search bar
    1. Press Advanced search to toggle between default and advanced search. Advanced search allows the user to search by name and ID
3. To select an existing patient, press anywhere inside the patient's list item.
4. To delete an existing patient, select the delete button inside the patient's list item.

![Patient List Page](https://user-images.githubusercontent.com/44624435/230219923-d36b345d-eec3-4538-819f-e55752291e30.png)

### 2.2 Patient Form Page

- Fill in patient parameters 
- Press Save to add the new patient to the list
- Press Cancel to return to the Patient List Page

![image](https://user-images.githubusercontent.com/44624435/230220126-69396a73-789b-462c-8148-f99022ee2b2b.png)


### 2.3 Patient Information Page

- Press Edit to change patient parameters.
- If there is new data, input the prescribed dosage, ANC measurement and date of measurement.
- Press Save to save the record into the database.
- Input the number of cycles into the future to run
- Press Calculate to run the model with the newest and previously saved records. 
- Press Cancel to return to the Patient List Page

![image](https://user-images.githubusercontent.com/44624435/230220395-b7f8dfa9-6d76-401e-8e1f-6c42c81ceeed.png)

Navigate to other pages by pressing the icons on the left. If the model has already been run for the patient, the user can return to the dashboard without running the model again by pressing the Dashboard icon on the left. 

![tab legend](https://user-images.githubusercontent.com/44624435/230222852-0e2b3d38-e36b-417c-b5ba-2b42753016fa.png)

### 2.4 Dashboard

The model can take a few minutes (4-5 minutes per cycle) to complete and the application will say it is not responding. This is normal.

![image](https://user-images.githubusercontent.com/44624435/226801521-8a6a05b7-9332-4b66-bea4-fbf06a8e1651.png)

Navigate to previous pages using the tabs on the left.

## 3.0 Matlab Model

The Matlab Model is called through `runModel()` found in `matlab_script.py`. It calls `runController.m` found in the `/Leukemia-Treatment-Project` directory 

## 4.0 Optional: Create a new user

To create a new user, login with credentials: username: admin, password: admin

Then click on the plus icon in the top left.

![image](https://user-images.githubusercontent.com/44624435/230220785-ed69bebe-98d0-4843-8056-8ba1e72cbae4.png)

Fill out the form and press save to complete registration.

![image](https://user-images.githubusercontent.com/44624435/226797182-f944154d-26f6-49cb-be06-4cd3216e4d7f.png)

Logout from the admin account and login with the newly created account.


