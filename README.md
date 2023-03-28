# Leukemia-Treatment-Application

## Pre-requisites

- Python >= 3.6.1
- Matlab >= R2022b

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
Login with credentials. To create a new user, see section 3.0

![image](https://user-images.githubusercontent.com/44624435/226797287-7ec91a25-df3c-48b4-99d3-2bb32287f7fa.png)

After logging in, log out at any time by pressing the `Log Off` button in the top right of the application. 


### 2.1 Patient List Page

1. To create a patient profile, click on the plus icon in the top left.
2. To search for an existing patient, type into the search bar and press 'Advanced Search'.
3. To select an existing patient, press anywhere inside the patient's list item.
4. To delete an existing patient, select the delete button inside the patient's list item.

![Patient List Page](https://user-images.githubusercontent.com/44624435/226800089-e491592e-f9ed-4417-90a1-fd3659bde801.png)

### 2.2 Patient Form Page

- Fill in patient parameters 
- Press Save to add the new patient to the list
- Press OK to continue with this patient to the Patient Information Page
- Press Cancel to return to the Patient List Page

![image](https://user-images.githubusercontent.com/44624435/226801284-dfb7096f-3010-4cbb-bda2-81186fad0a2c.png)


### 2.3 Patient Information Page

- Press Edit to change patient parameters.
- If there is new data, input the prescribed dosage, ANC measurement and date of measurement.
- Press Save to save the record into the database.
- Press OK to run the model with the newest and previously saved records. 
- Press Cancel to return to the Patient List Page

![image](https://user-images.githubusercontent.com/44624435/226800259-ca3993db-3005-405a-92e2-64c54bf62462.png)

### 2.4 Dashboard

The model can take a few minutes (4-5 minutes per cycle) to complete, this is normal.

![image](https://user-images.githubusercontent.com/44624435/226801521-8a6a05b7-9332-4b66-bea4-fbf06a8e1651.png)

## 3.0 Matlab Model

The Matlab Model is called through `runModel()` found in `matlab_script.py`. It calls `runController.m` found in the `/Leukemia-Treatment-Project` directory 

## 4.0 Optional: Create a new user

To create a new user, login with credentials: username: admin, password: admin

Then click on the plus icon in the top left.

![image](https://user-images.githubusercontent.com/44624435/226797151-510f8520-61a2-4c54-9a09-2142115293e0.png)

Fill out the form and press save to complete registration.

![image](https://user-images.githubusercontent.com/44624435/226797182-f944154d-26f6-49cb-be06-4cd3216e4d7f.png)

Logout from the admin account and login with the newly created account.


