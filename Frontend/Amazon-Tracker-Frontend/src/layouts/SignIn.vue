<template>
  <div class="container" id="content">
    <form>
      <h2 class="mb-3">Login</h2>
      <div class="input">
        <label for="email">Email address</label>
        <input
          class="form-control"
          type="text"
          v-model="email"
          placeholder="email@adress.com"
        />
      </div>
      <div class="input">
        <label for="password">Password</label>
        <input
          class="form-control"
          type="password"
          v-model="password"
          placeholder="password123"
        />
      </div>
      <q-item to="/register" class="alternative-option mt-4">
        <q-item-label>Don't have an account? Register Here!!</q-item-label>
      </q-item>
      <p v-if="errMsg">{{ errMsg }}</p>
      <button @click="signInUser" class="mt-4 btn-pers" id="login_button">
        Login
      </button>
    </form>
  </div>
</template>

<script>
import {ref} from "vue";
import {getAuth, GoogleAuthProvider, signInWithEmailAndPassword, signInWithPopup} from "firebase/auth" ;
import {useRouter} from "vue-router";
import axios from "axios";
import {useStore} from "vuex";

export default {
  name: "SignIn",
  setup() {
    const email = ref("");
    const password = ref("");
    const router = useRouter();
    const errMsg = ref();
    const auth = getAuth();
    const apiUrl = "http://13.57.224.247:5000/login";
    const apiUrl1 = "http://13.57.224.247:5000/fetchCards";

    const store = useStore();

    const signInUser = () => {
      signInWithEmailAndPassword(auth, email.value, password.value)
        .then((data) => {
          console.log("Successfully registered!");
          store.dispatch("amazon/updateEmailId", email.value);

          getFullNameFromDB(email.value).then((curr_name) => {
            store.dispatch("amazon/updateFullName", curr_name);
          });

          getCardsInStore(email.value).then((card_detail) => {
            if (card_detail.length !== 0) {
              for (let i = 0; i < card_detail.length; i++) {
                store.dispatch("amazon/updateCardDetail", card_detail[i]);
              }
            }
          });
          router.push("/search");
        }).catch((error) => {
        console.log(error.code);
        alert(error.message);
        switch (error.code) {
          case "auth/invalid-email":
            errMsg.value = "Invalid email";
            break;
          case "auth/user-not-found":
            errMsg.value = "No account with that email was found";
            break;
          case "auth/wrong-password'" :
            errMsg.value = " Incorrect password";
            break;
          default:
            errMsg.value = "Email or password was incorrect";
            break;
        }

      });
    };

    const getFullNameFromDB = async (email) => {
      console.log("in the db function");
      try {
        const response = await axios.put(apiUrl, {
          email
        });
        console.log(response.data.full_name); // logs the response from the server
        return response.data.full_name;
      } catch (error) {
        console.error(error);
      }
    };

    const getCardsInStore = async (email) => {
      try {
        const response = await axios.put(apiUrl1, {
          email
        });
        return response.data;
      } catch (error) {
        console.error(error);
      }
    };
    const signInWithGoogle = () => {
      const provider = new GoogleAuthProvider();
      signInWithPopup(getAuth(), provider).then((result) => {
        console.log(result.user);
        router.push("/search");
      }).catch((error) => {
        // handle error
        console.log(error);
      });
    };

    return {
      signInUser,
      signInWithGoogle,
      email,
      password,
      errMsg
    };
  }
};
</script>

<style scoped>

</style>
