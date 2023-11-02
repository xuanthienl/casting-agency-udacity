<template>
    <div class="container p-2">
        <div class="row m-2">
            <div class="col p-0">
                <div class="box-custom m-2">
                    <form @submit.prevent="Submit">
                        <div>
                            <select v-model="movie" required>
                                <option disabled value="">Select Movie</option>
                                <option :value="item.id" v-for="(item, index) in movies" :key="index">{{ item.title }}
                                </option>
                            </select>
                            <select v-model="actor" required>
                                <option disabled value="">Select Actor</option>
                                <option :value="item.id" v-for="(item, index) in actors" :key="index">{{ item.name }}
                                </option>
                            </select>
                        </div>
                        <div class="d-flex justify-content-end">
                            <button type="submit" class="btn">
                                <font-awesome-icon icon="floppy-disk" />
                                Save
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            backEndUrl: process.env.VUE_APP_BACKEND_URL,
            movies: [],
            actors: [],
            movie: '',
            actor: ''
        }
    },
    mounted() {
        this.axios
            .get(this.backEndUrl + '/movies', {
                headers: {
                    Authorization: `Bearer ${this.$store.state.token}`
                },
            })
            .then(result => {
                this.movies = result.data.data
            })
            .catch(error => {
                this.Notify(error.response.data.error)
            });

        this.axios
            .get(this.backEndUrl + '/actors', {
                headers: {
                    Authorization: `Bearer ${this.$store.state.token}`
                },
            })
            .then(result => {
                this.actors = result.data.data
            })
            .catch(error => {
                this.Notify(error.response.data.error)
            });
    },
    methods: {
        Submit(e) {
            e.preventDefault();
            this.axios
                .post(this.backEndUrl + '/casting', {
                    movie: this.movie,
                    actor: this.actor
                }, {
                    headers: {
                        Authorization: `Bearer ${this.$store.state.token}`
                    },
                })
                .then(result => {
                    this.actor = ''
                    this.movie = ''
                    this.$notify({
                        group: 'foo',
                        title: 'OK.',
                        duration: 10000,
                        speed: 1000
                    });
                    return result
                })
                .catch(error => {
                    this.Notify(error.response.data.error)
                });
        },
        Notify(code) {
            var message = 'FAIL.'
            if (code == '403') {
                message += ' You do not have the required permissions to perform this action.'
            }
            else if (code == '404') {
                message += ' The resource you requested cannot be found.'
            }
            else if (code == '422') {
                message += ' The data you entered is invalid. Please review and try again.'
            }
            else {
                message += ' An unexpected error occurred.'
            }
            this.$notify({
                group: 'foo',
                title: message,
                duration: 10000,
                speed: 1000
            });
        }
    }
}
</script>
