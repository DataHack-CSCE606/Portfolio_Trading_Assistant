<template>
  <div class="signup-buttons">
    <a href="#" class="google-signup" @click.prevent="loginWithGoogle">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="18"
        height="18"
        viewBox="0 0 18 18"
        aria-hidden="true"
      >
        <title>Google</title>
        <g fill="none" fill-rule="evenodd">
          <path
            fill="#4285F4"
            d="M17.64 9.2045c0-.6381-.0573-1.2518-.1636-1.8409H9v3.4814h4.8436c-.2086 1.125-.8427 2.0782-1.7959 2.7164v2.2581h2.9087c1.7018-1.5668 2.6836-3.874 2.6836-6.615z"
          ></path>
          <path
            fill="#34A853"
            d="M9 18c2.43 0 4.4673-.806 5.9564-2.1805l-2.9087-2.2581c-.8059.54-1.8368.859-3.0477.859-2.344 0-4.3282-1.5831-5.036-3.7104H.9574v2.3318C2.4382 15.9832 5.4818 18 9 18z"
          ></path>
          <path
            fill="#FBBC05"
            d="M3.964 10.71c-.18-.54-.2822-1.1168-.2822-1.71s.1023-1.17.2823-1.71V4.9582H.9573A8.9965 8.9965 0 0 0 0 9c0 1.4523.3477 2.8268.9573 4.0418L3.964 10.71z"
          ></path>
          <path
            fill="#EA4335"
            d="M9 3.5795c1.3214 0 2.5077.4541 3.4405 1.346l2.5813-2.5814C13.4632.8918 11.426 0 9 0 5.4818 0 2.4382 2.0168.9573 4.9582L3.964 7.29C4.6718 5.1627 6.6559 3.5795 9 3.5795z"
          ></path>
        </g>
      </svg>
      Google
    </a>
  </div>
</template>

<script>
import router from "@/router/router";
import axios from "axios";
export default {
  name: "login_signup_social",
  mounted() {},
  methods: {
    loginWithGoogle() {
      this.$gAuth
        .signIn()
        .then((GoogleUser) => {
          // on success do something
          // console.log("GoogleUser", GoogleUser);
          // console.log("getId", GoogleUser.getId());
          // console.log("getBasicProfile", GoogleUser.getBasicProfile());
          // console.log("getAuthResponse", GoogleUser.getAuthResponse());
          var id_token = GoogleUser.getAuthResponse().id_token;
          axios
            .post("/login/", {
              id_token: id_token,
            })
            .then((res) => {
              // console.log(res);
              var profile = GoogleUser.getBasicProfile();
              var userInfo = {
                id: profile.getId(),
                name: profile.getName(),
                imageUrl: profile.getImageUrl(),
                email: profile.getEmail(),
                auth: GoogleUser.getAuthResponse(),
                user_id: res.data.user_id,
              };
              this.$store.commit("setLoginUser", userInfo);
              router.push("/home");
            })
            .catch((err) => {
              console.error(err);
            });
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
  },
};
</script>

<style lang="sass" scoped>
.signup-buttons
  margin-top: 15px
  display: -webkit-box
  display: -ms-flexbox
  display: flex
  -webkit-box-pack: justify
  -ms-flex-pack: justify
  justify-content: space-between
  position: relative

.facebook-signup,
.google-signup
  color: #031b4e
  background: #f2f8ff
  border: 1px solid rgba(0, 105, 255, .2)
  -webkit-box-sizing: border-box
  box-sizing: border-box
  border-radius: 3px
  display: inline-block
  margin-top: 0
  width: 100%
  padding: 15px
  text-align: center
  position: inherit

.signup-buttons a
  vertical-align: middle
  text-decoration: none

.signup-buttons svg
  left: 16px
  position: absolute
  top: 50%
  -webkit-transform: translateY(-50%)
  transform: translateY(-50%)

.footer,
.footer a
  text-align: center
  color: #fff
</style>>