<script>
  // Navbar와 Footer 컴포넌트를 가져옴
  import Navbar from './components/Navbar.svelte';
  import Footer from './components/Footer.svelte';

  // 플로팅 버튼 함수
  import FloatingButton from './components/FloatingButton.svelte';

  // 라우터 연결
  import Router from 'svelte-spa-router';
  import Home from "./routes/Home.svelte";
  import Join from './routes/Join.svelte';
  import Login from './routes/Login.svelte';
  import AIIntro from "./routes/AIIntro.svelte";
  import AIChat from "./routes/AIChat.svelte";
  import ShoppingList from "./routes/ShoppingList.svelte";
  import SpotList from "./routes/SpotList.svelte";
  import SpotView from './routes/SpotView.svelte';
  import FestList from './routes/FestList.svelte';
  import FestView from './routes/FestView.svelte';
  import ReviewList from './routes/ReviewList.svelte';
  import ReviewInsert from './routes/ReviewInsert.svelte';
  import ReviewView from './routes/ReviewView.svelte';
  import ReviewUpdate from './routes/ReviewUpdate.svelte';
  import MyChatlogList from './routes/myChatlogList.svelte';
  import MyChatlogView from './routes/myChatlogView.svelte';
  import MyReviewList from './routes/myReviewList.svelte';
  import MyReviewView from './routes/myReviewView.svelte';
  import MyInfoUpdate from './routes/myInfoUpdate.svelte';

  const routes = {
  '/': Home,
  '/Join/': Join,
  '/Login/': Login,
  '/AI/': AIIntro,
  '/AIChat/': AIChat,
  '/Shopping/': ShoppingList,
  '/Spot/': SpotList,
  '/SpotView/': SpotView,
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
  '/MyInfo/': MyInfoUpdate
  }
  
</script>

<!-- 전체 페이지 구성 -->
<div class="d-flex flex-column">
  <!-- 헤더 -->
  <Navbar />

  <!-- 메인 컨텐츠 영역 : 여기에 페이지 컨텐츠 넣기 -->
  <main>
    <Router {routes}/>
  </main>

  <!-- 푸터 -->
  <Footer />

  <!-- 플로팅 버튼 -->
  <FloatingButton />
</div>
