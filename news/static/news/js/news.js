var category = document.querySelector("#category").textContent;
var pageIndex = 1
Vue.createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            newsList: {},
        }
    },
//    mounted(){
//        console.log(category);
//        axios.post('/api/news-list/', {'category': category})
//            .then(response => {
//                newsList = response.data;
//                totalNews = Object.keys(newsList).length;
//                this.newsDisplay = newsList.slice(0, showNews);
//                console.log(totalNews);
//            })
//            .catch(function (error) {
//                console.log(error);
//            });
//    },
    methods: {
        fetchMoreNews(event) {
            pageIndex += 1;
            axios.post('/api/news-list/', {'category': category, 'page': pageIndex})
            .then(response => {
                this.newsList = response.data;
                console.log(this.newsList);
            })
            .catch(function (error) {
                console.log(error);
            });
            if (pageIndex >= 10) {
                event.target.style.display = "none";
            };
        },
    }
}).mount('#app')