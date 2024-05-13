// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import {getFirestore} from "firebase/firestore"
import { getAuth } from "firebase/auth";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyCv7GuzB8LgbJxTbUHjw37lnSsCDcsOLcY",
  authDomain: "sqltodotest.firebaseapp.com",
  projectId: "sqltodotest",
  storageBucket: "sqltodotest.appspot.com",
  messagingSenderId: "493128325162",
  appId: "1:493128325162:web:9269b7240ad83c01f04b53"
};




// Initialize Firebase
const app = initializeApp(firebaseConfig);

export const db = getFirestore(app)
export const auth = getAuth(app);