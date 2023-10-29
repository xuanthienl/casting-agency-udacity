<template>
    <div class="container" id="app">
        <TheHeader/>
        <router-view></router-view>
        <notifications class="notifications" group="foo"/>
    </div>
</template>

<script>
import TheHeader from './components/TheHeader.vue'

export default {
    name: 'App',
    components: {
        TheHeader
    }
}
</script>
