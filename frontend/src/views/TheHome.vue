<template>
    <div class="p-5">
        <p class="text-center text-custom">Welcome to Casting Agency Group</p>
        <div class="d-flex justify-content-center align-items-center ">
            <button type="button" class="mx-3" v-on:click="MoviesPage()">
                <font-awesome-icon icon="video" />
                Add new Movies
            </button>
            <button type="button" class="mx-3" v-on:click="ActorsPage()">
                <font-awesome-icon icon="child" />
                Add new Actors
            </button>
        </div>
    </div>
</template>

<script>
export default {
    methods: {
        MoviesPage() {
            this.$router.push({ name: 'movies' })
        },
        ActorsPage() {
            this.$router.push({ name: 'actors' })
        }
    }
}
</script>
