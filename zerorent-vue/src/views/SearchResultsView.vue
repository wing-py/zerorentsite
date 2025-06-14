<template>
  <div class="search-results-container">
	<n-card class="main-content">
	  <template #header>
		<h2 class="text-h5">搜索结果: "{{ searchQuery }}"</h2>
	  </template>

	  <div class="card-text-content">
		<div class="search-bar d-flex align-center mb-4">
		  <n-input
			v-model:value="searchQuery"
			placeholder="搜索信函..."
			clearable
			class="mr-2"
		  />
		  <n-button type="primary" @click="performSearch">搜索</n-button>
		</div>

		<n-list v-if="letters && letters.length > 0" hoverable clickable>
		  <n-list-item v-for="letter in letters" :key="letter.id" @click="goToLetterDetail(letter.id)">
			<n-thing
			  :title="letter.title"
			  :description="formatLetterSubtitle(letter)"
			>
			  <p class="text-body-2 mt-2">{{ truncateContent(letter.content) }}</p>
			</n-thing>
		  </n-list-item>
		</n-list>
		<div v-else class="text-center text-body-1 grey-text">
		  <p class="no-results translatable">没有找到与 "{{ searchQuery }}" 相关的信函</p>
		</div>
	  </div>
	</n-card>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { NCard, NInput, NButton, NList, NListItem, NThing } from 'naive-ui';
import type {letterType} from './LetterDetailView.vue';
import type { LocationQueryValue } from "vue-router";

const route = useRoute();
const router = useRouter();

const searchQuery = ref<string|null>(Array.isArray(route.query.q)?'':route.query.q);
// const searchQuery = ref<string|null>( null);

const letters=ref<letterType[]>([
		{ id: 1,
			title: '搜索结果示例',
			category: '问题反馈',
			created_at: '2023-10-26 10:00',
			author: { username: '搜索作者' },
			content: '这是与您的搜索相关的示例信函内容，非常长，需要截断显示。这是与您的搜索相关的示例信函内容，非常长，需要截断显示。',
			attachments:null,
			display_permission:'',
			ip_address:'127.0.0.1',
		}
	  ]);

watch(
	() => route.query.q,
  (newQuery) => {
	// 处理可能的数组类型（当URL中有多个q参数时）
		const normalizedQuery:string|null = Array.isArray(newQuery)
			? null
			: newQuery;
		searchQuery.value = normalizedQuery;
		performSearch();
	},
	{immediate:true}
);

const performSearch = () => {
	  console.log('Performing search for:', searchQuery.value);
	  // Implement search logic here based on this.searchQuery
	};
const goToLetterDetail = (id:number) => {
	  router.push('/mailbox/' + id);
	};

const formatLetterSubtitle = (letter:letterType):string => {
	  let subtitle:string = `${letter.category} ${letter.created_at}`;
	  if (letter.author) {
		subtitle += ` 作者: ${letter.author.username}`;
	  }
	  return subtitle;
	};

const truncateContent = (content:string):string => {
	  const maxLength = 100;
	  return content.length > maxLength ? content.substring(0, maxLength) + '...' : content;
	}

onMounted(() => {
	if (searchQuery.value) {
	  performSearch();
	}
  })

// export default {
//   name: 'SearchResultsView',
//   components: {
//     NCard,
//     NInput,
//     NButton,
//     NList,
//     NListItem,
//     NThing
//   },
//   data() {
//     return {
//       searchQuery: this.$route.query.q || '',
//       letters: [
//         { id: 1, title: '搜索结果示例', category: '问题反馈', content: '这是与您的搜索相关的示例信函内容，非常长，需要截断显示。这是与您的搜索相关的示例信函内容，非常长，需要截断显示。', created_at: '2023-10-27 12:00', author: { username: '搜索作者' } }
//       ]
//     };
//   },
//   watch: {
//     '$route.query.q'(newQuery) {
//       this.searchQuery = newQuery;
//       this.performSearch();
//     }
//   },
//   methods: {
//     performSearch() {
//       console.log('Performing search for:', this.searchQuery);
//       // Implement search logic here based on this.searchQuery
//     },
//     goToLetterDetail(id) {
//       this.$router.push('/mailbox/' + id);
//     },
//     formatLetterSubtitle(letter) {
//       let subtitle = `${letter.category} ${letter.created_at}`;
//       if (letter.author) {
//         subtitle += ` 作者: ${letter.author.username}`;
//       }
//       return subtitle;
//     },
//     truncateContent(content) {
//       const maxLength = 100;
//       return content.length > maxLength ? content.substring(0, maxLength) + '...' : content;
//     }
//   },
//   mounted() {
//     if (this.searchQuery) {
//       this.performSearch();
//     }
//   }
// }
</script>

<style scoped>
.search-results-container {
  padding: 20px;
}

.main-content {
  max-width: 900px;
  margin: 0 auto;
}

.text-h5 {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 20px;
}

.card-text-content {
  padding: 16px;
}

.search-bar {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}

.mr-2 {
  margin-right: 8px;
}

.text-center {
  text-align: center;
}

.text-body-1 {
  font-size: 1rem;
  line-height: 1.6;
}

.text-body-2 {
  font-size: 0.875rem;
  line-height: 1.6;
}

.grey-text {
  color: #9aa0a6;
}

.no-results {
  margin-top: 20px;
}
</style>