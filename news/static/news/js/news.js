var category = document.querySelector("#category").textContent;
var newsList
var totalNews
var showNews = 10
Vue.createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            newsDisplay: null,
        }
    },
    mounted(){
        console.log(category);
        axios.post('/api/news-list/', {'category': category})
            .then(response => {
                newsList = response.data;
                totalNews = Object.keys(newsList).length;
                this.newsDisplay = newsList.slice(0, showNews);
                console.log(totalNews);
            })
            .catch(function (error) {
                console.log(error);
            });
    },
    methods: {
        showMoreNews(event) {
            showNews += 10;
            this.newsDisplay = newsList.slice(0, showNews);
            if (showNews >= totalNews) {
                event.target.style.display = "none";
            };
        },
    }
}).mount('#app')