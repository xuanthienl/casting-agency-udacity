<script>
export default {
    created() {
        this.$store.dispatch('setJWT', window.location.hash)
    }
}
</script>
