<template>
    <div class="h-100 d-flex justify-content-center">
        <div class="row my-auto box-custom">
            <div class="box-text">
                <h4 class="m-0">Sign In</h4>
                <p class="m-0">to Casting Agency</p>
            </div>
            <form @submit.prevent="Submit">
                <div>
                    <input type="text" v-model="username" placeholder="Username/Email" required>
                    <input type="text" v-model="password" placeholder="Password" required>
                </div>
                <div class="d-flex justify-content-end">
                    <button type="submit" class="btn">
                        <font-awesome-icon icon="arrow-right-to-bracket" />
                        Log In
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            backEndUrl: process.env.VUE_APP_BACKEND_URL,
            username: '',
            password: ''
        }
    },
    methods: {
        Submit(e) {
            e.preventDefault();
            this.axios
                .post(this.backEndUrl + '/login', {
                    username: this.username,
                    password: this.password
                })
                .then(result => {
                    this.$store.dispatch('setJWT', result.data.data)
                })
                .catch(error => {
                    this.$notify({
                        group: 'foo',
                        title: 'FAIL. Please check your username and password.',
                        duration: 10000,
                        speed: 1000
                    });
                    console.log(error)
                });
        },
    }
}
</script>
