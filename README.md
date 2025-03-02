# **GuideAI: AI-Powered Tourist Guide**  

## **Overview**  
**GuideAI** is an AI-based travel assistant that helps users find locations, plan trips, get real-time navigation, and explore activities. It leverages AI for enhanced recommendations and smooth travel experiences.  

This project was developed in collaboration with my friend during the **IBM State-Level Hackathon**, where we built an AI-powered travel guide to assist tourists with seamless navigation, trip planning, and real-time updates. 🚀  

## **Features**  
- ✅ **Live Location Tracking** – Get real-time location updates.  
- ✅ **Trip Planning** – AI-powered itinerary suggestions.  
- ✅ **Navigation Assistance** – Find the best routes and directions.  
- ✅ **Activity Recommendations** – Discover places to visit and things to do.  
- ✅ **Multilingual Support** – Interact in multiple languages for a better user experience.  
- ✅ **AI-Powered Image Recognition** – Upload an image to get relevant location details.  
- ✅ **IBM Watson Integration** – Uses AI-powered services for natural language understanding.  

---

## **Tech Stack**  
- **Backend:** Flask (Python)  
- **Frontend:** HTML, CSS, JavaScript  
- **Database:** MongoDB  
- **AI Services:** IBM Watson, Google APIs  
- **Hosting:** IBM Cloud  

---

## **Installation**  

### **1. Clone the Repository**  
```bash
git clone https://github.com/UnbeatableBann/GuideAI.git
cd GuideAI
```  

### **2. Create a Virtual Environment**  
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```  

### **3. Install Dependencies**  
```bash
pip install -r requirements.txt
```  

### **4. Set Up Environment Variables**  
Create a `.env` file and add your API keys:  
```ini
API_KEY=your_google_api_key
IBM_WATSON_KEY=your_ibm_watson_key
SECRET_KEY=your_secret_key
DATABASE_URI=your_mongodb_uri
```  

### **5. Run the Application**  
```bash
python app.py
```  
Open [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser.  

---

## **Screenshots**  

### **1️⃣ IBM Login Page**  
![Project Screenshot](Screenshots/Login.png)  

### **2️⃣ Multilingual Support**  
![Project Screenshot](Screenshots/Multilingual.png)  
![Project Screenshot](Screenshots/Multilingual2.png)  

### **3️⃣ AI-Powered Image Recognition**  
![Project Screenshot](Screenshots/UploadImage.png)  

### **4️⃣ Trip Planning**  
![Project Screenshot](Screenshots/TripPlanning.png)  

---

## **Usage**  
1. **Enter your current location** – The AI will track your position.  
2. **Select a destination** – Get AI-powered recommendations.  
3. **Receive navigation assistance** – Best routes and travel options.  
4. **Upload an image** – The AI identifies places based on the image.  
5. **Multilingual support** – Interact in different languages.  

---

## **File Structure**  
```
GuideAI/
│── static/                  # Contains static assets like CSS, JavaScript, and images
│── templates/               # HTML templates for rendering web pages
│── .flask_session/          # Flask session storage
│── .env                     # Environment variables (Do not share publicly)
│── .gitignore               # Specifies files to ignore in version control
│── app.py                   # Main application file
│── image.py                 # Handles image processing for location recognition
│── livelocation.py          # Fetches real-time location data
│── trip_planning.py         # AI-based trip planner
│── requirements.txt         # Dependencies required for the project
└── README.md                # Project documentation
```

---

## **Security Considerations**  
🔴 **Important:** To protect sensitive data, ensure the following files are **not shared publicly**:  
- `.env` (Contains API keys and secret credentials)  
- Any files containing **private API keys** or **database credentials**  

Ensure that `.gitignore` includes:  
```
.env
__pycache__/
.flask_session/
.ipynb_checkpoints/
```

---

## **Hackathon Experience 🎯**  
GuideAI was developed as part of the **IBM State-Level Hackathon**, where my friend and I collaborated to create an AI-driven travel assistant. Our goal was to enhance tourism experiences using AI and real-time data, providing travelers with smarter and more interactive solutions.  

During the hackathon, we integrated **IBM Watson services** for **AI-powered responses**, implemented **Google APIs** for location tracking, and built an intuitive **Flask-based backend**. Our teamwork and innovation helped us build a project that could transform how tourists explore new places! 🌍  

---

## **Contributing**  
We welcome contributions! Follow these steps to contribute:  
1. **Fork** the repository.  
2. **Create a branch** for your feature (`git checkout -b feature-name`).  
3. **Commit your changes** (`git commit -m "Added new feature"`).  
4. **Push to the branch** (`git push origin feature-name`).  
5. **Open a pull request**.  

We will review your contributions and merge them if they align with the project goals. 🚀  

---

## **License**  
This project is licensed under the **MIT License**.  

---

## **Contact**  
For any queries, feel free to reach out:  
📧 Email: [your-email@example.com](mailto:shadabjamadaar4@gmail.com)  
🌐 GitHub: [UnbeatableBann](https://github.com/UnbeatableBann)  

---

🚀 **Happy Coding & Safe Travels!** 🌍  
