 // 라우터 연결
 import Home from "../../routes/Home.svelte";
 import Join from '../../routes/Join.svelte';
 import Login from '../../routes/Login.svelte';
 import AIIntro from "../../routes/AIIntro.svelte";
 import AIChat from "../../routes/AIChat.svelte";
 import ShoppingList from "../../routes/ShoppingList.svelte";
 import SpotList from "../../routes/SpotList.svelte";
 import SpotView from '../../routes/SpotView.svelte';
 import FestList from '../../routes/FestList.svelte';
 import FestView from '../../routes/FestView.svelte';
 import ReviewList from '../../routes/ReviewList.svelte';
 import ReviewInsert from '../../routes/ReviewInsert.svelte';
 import ReviewView from '../../routes/ReviewView.svelte';
 import ReviewUpdate from '../../routes/ReviewUpdate.svelte';
 import MyChatlogList from '../../routes/myChatlogList.svelte';
 import MyChatlogView from '../../routes/myChatlogView.svelte';
 import MyReviewList from '../../routes/myReviewList.svelte';
 import MyReviewView from '../../routes/myReviewView.svelte';
 import MyInfoUpdate from '../../routes/myInfoUpdate.svelte';
 import test from '../../routes/test.svelte';

 const routes = {
   '/': Home,
   '/Join/': Join,
   '/Login/': Login,
   '/AI/': AIIntro,
   '/AIChat/': AIChat,
   '/Shopping/': ShoppingList,
   '/Spot/': SpotList,
   '/SpotView/:POI_IDX': SpotView,
   '/Fest/': FestList,
   '/FestView/': FestView,
   '/Review/': ReviewList,
   '/ReviewInsert/': ReviewInsert,
   '/ReviewView/': ReviewView,
   '/ReviewUpdate/': ReviewUpdate,
   '/My/': MyChatlogList,
   '/MyChatlogView/': MyChatlogView,
   '/MyReview/': MyReviewList,
   '/MyReviewView/': MyReviewView,
   '/MyInfo/': MyInfoUpdate,
 };

 export default routes;