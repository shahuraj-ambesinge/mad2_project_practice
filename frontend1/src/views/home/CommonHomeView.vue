<template>
    <div>
        <nav class="navbar navbar-expand-lg bg-body-tertiary">
            <div class="container-fluid">
                <a class="navbar-brand" href="#">Kanban</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
                    data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false"
                    aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                        <li class="nav-item">
                            Welcome {{ user_mail }}
                        </li>
                    </ul>

                </div>
            </div>
        </nav>
        <div>
            <div class="container text-center">
                <div class="row">
                    <div class="col-1">
                    
                    </div>
                    <div class="col-10">
                        <button type="button" class="btn btn-warning" style="border-radius: 5rem; font-size: large;">+</button>
                        <div v-for="list in all_lists" :key="list.list_id">
                            <div class="card ms-1 float-start" style="width: 18rem; margin: 10px">
                                <div class="card-body">
                                    <h4 class="card-title">{{ list.list_id }}</h4>
                                    <h6 class="card-subtitle mb-2 text-body-secondary">{{ list.list_name }}</h6>
                                    <p class="card-text">{{ list.list_disc }}</p>
                                    <!-- <a href="#" class="card-link">Card link</a>
                                    <a href="#" class="card-link">Another link</a> -->
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="col-1">
                    
                    </div>
                    {{ all_lists }}
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import refreshAccessToken from '../../utils/refreshToken'

export default {
    name: "UserHomeView",
    data() {
        return{
            user_mail:"",
            all_lists:[]
        }
    },
    created(){
        this.allList()
    },
    methods:{
        async allList(){
            try{
                this.user_mail = localStorage.getItem('user_mail')
                let access_token = localStorage.getItem('access_token')

                axios.defaults.headers.common['Authorization'] = "Bearer " + access_token
                axios.get('http://127.0.0.1:8081/api/list').then((response) =>{
                    console.log(response.data)
                    this.all_lists = response.data
                })
                

            }
            catch(error){
                if (error.response && error.response.status ===401){
                    await refreshAccessToken()
                    await this.allList()
                }
                else if (error.response){
                    console.error(error)
                    alert("an error occured while fetching data")
                }


            }

            }
            
        }
    }



</script>

<style scoped></style>