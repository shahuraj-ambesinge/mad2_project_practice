<template>
    <div>
        <h3>Hello........</h3>
        {{ this.mail }}
        {{ this.pass }}

    </div>
</template>

<script>
export default {
    name:"userHeader",
    props: {
        mail:String,
        pass:String,
    }

}
</script>

<style scoped></style>