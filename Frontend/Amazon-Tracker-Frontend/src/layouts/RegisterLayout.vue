<template>

  <div class="container" id="content">
    <form>
      <h2 class="mb-3">SignUp</h2>
      <div class="input">
        <label for="email">Full Name</label>
        <input
          class="form-control"
          type="text"
          v-model="fullName"
          placeholder="User Name"
        />
      </div>
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
      <q-item to="/sign-in">
        <q-item-label> Already an user? Login Here!!</q-item-label>
      </q-item>
      <p v-if="errMsg">{{ errMsg }}</p>
      <button @click="registerUser" class="mt-4 btn-pers" id="login_button">
        Register
      </button>
    </form>
  </div>
</template>
