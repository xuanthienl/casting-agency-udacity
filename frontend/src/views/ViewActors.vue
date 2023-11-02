<template>
    <div class="container p-2">

        <button type="button" class="mx-3" v-on:click="Show()">
            <font-awesome-icon icon="fa-feather-alt" />
            Add new actors
        </button>

        <div class="row m-2">
            <div class="col col-md-3 p-0" v-for="(item, index) in items" :key="index">
                <div class="box-custom m-2">
                    <div class="box">
                        <p class="m-0">Name: {{ item.name }}</p>
                        <p class="m-0 text-display">Age: {{ item.age }} / Gender: {{ item.gender }}</p>
                        <p class="m-0">Movies: <span v-for="(movie, movieIndex) in item.movies" :key="movieIndex">{{ movieIndex + 1 != item.movies.length ? movie.title + ', ' : movie.title}}</span></p>
                    </div>
                    <div class="d-md-flex justify-content-between">
                        <button type="button" v-on:click="Edit(index)">
                            <font-awesome-icon icon="pencil" />
                            Edit
                        </button>
                        <button type="button" v-on:click="Delete(index)">
                            <font-awesome-icon icon="eraser" />
                            Delete
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <b-modal ref="Modal" centered hide-footer hide-header>
            <div class="d-flex justify-content-between align-items-center">
                <h5>
                    <font-awesome-icon icon="fa-feather-alt" />
                    <span class="px-3">{{ this.index == -1 ? "Create..." : "Update..." }}</span>
                </h5>
                <font-awesome-icon icon="fa-times" data-bs-dismiss="modal" v-on:click="Hide()" />
            </div>
            <form @submit.prevent="Submit">
                <div>
                    <input type="text" v-model="name" placeholder="Name" required>
                    <input type="text" v-model="age" placeholder="Age" required>
                    <select v-model="gender" required>
                        <option disabled value="">Gender</option>
                        <option value="male">Male</option>
                        <option value="female">Female</option>
                        <option value="other">Other</option>
                    </select>
                </div>
                <div class="d-flex justify-content-end">
                    <button type="submit" class="btn">
                        <font-awesome-icon icon="floppy-disk" />
                        Save
                    </button>
                </div>
            </form>
        </b-modal>

    </div>
</template>

<script>
export default {
    data() {
        return {
            backEndUrl: process.env.VUE_APP_BACKEND_URL,
            items: [],
            index: -1,
            name: '',
            age: '',
            gender: '',
        }
    },
    mounted() {
        this.axios
            .get(this.backEndUrl + '/actors', {
                headers: {
                    Authorization: `Bearer ${this.$store.state.token}`
                },
            })
            .then(result => {
                this.items = result.data.data
            })
            .catch(error => {
                this.Notify(error.response.data.error)
            });

        this.$root.$on('bv::modal::hide', () => {
            this.Clear()
        })
    },
    methods: {
        Submit(e) {
            e.preventDefault();
            if (this.index >= 0) {
                this.axios
                    .patch(this.backEndUrl + '/actors/' + this.items[this.index].id, {
                        name: this.name,
                        age: this.age,
                        gender: this.gender
                    }, {
                        headers: {
                            Authorization: `Bearer ${this.$store.state.token}`
                        },
                    })
                    .then(result => {
                        this.items[this.index].name = this.name
                        this.items[this.index].age = this.age
                        this.items[this.index].gender = this.gender
                        this.Hide()
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
                        this.Hide()
                    });
                return
            }
            this.axios
                .post(this.backEndUrl + '/actors', {
                    name: this.name,
                    age: this.age,
                    gender: this.gender
                }, {
                    headers: {
                        Authorization: `Bearer ${this.$store.state.token}`
                    },
                })
                .then(result => {
                    this.items.push(result.data.data)
                    this.$notify({
                        group: 'foo',
                        title: 'OK.',
                        duration: 10000,
                        speed: 1000
                    });
                    this.Hide()
                })
                .catch(error => {
                    this.Notify(error.response.data.error)
                    this.Hide()
                });
        },
        Edit(index) {
            this.index = index
            this.name = this.items[index].name
            this.age = this.items[index].age
            this.gender = this.items[index].gender
            this.Show()
        },
        Delete(index) {
            this.axios
                .delete(this.backEndUrl + '/actors/' + this.items[index].id, {
                    headers: {
                        Authorization: `Bearer ${this.$store.state.token}`
                    },
                })
                .then(result => {
                    this.items.splice(index, 1)
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
        Show() {
            this.$refs['Modal'].show()
        },
        Hide() {
            this.$refs['Modal'].hide()
            this.Clear()
        },
        Clear() {
            this.index = -1
            this.name = ''
            this.age = ''
            this.gender = ''
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
