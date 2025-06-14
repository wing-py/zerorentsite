<script lang="ts" setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { NCard, NForm, NFormItem, NInput, NButton, useDialog } from 'naive-ui'
import { isLogined } from '../App.vue'
import axios from 'axios'

const router = useRouter()
const dialog = useDialog()

dialog.warning({
  title: '注销',
  positiveText: '确认',
  negativeText: '不确认',
  draggable: true,
  onPositiveClick: () => {
    isLogined.value = false
  },
  onNegativeClick: () => {},
})

router.push('/')
</script>
