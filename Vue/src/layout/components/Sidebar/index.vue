<template>
  <div :class="{'has-logo':showLogo}">
    <logo v-if="showLogo" :collapse="isCollapse" />
    <users v-show="! isCollapse" />
    <el-scrollbar wrap-class="scrollbar-wrapper">
      <el-menu
        :default-active="activeMenu"
        :collapse="isCollapse"
        :background-color="variables.menuBg"
        :text-color="variables.menuText"
        :unique-opened="true"
        :active-text-color="variables.menuActiveText"
        :collapse-transition="false"
        mode="vertical"
      >
        <sidebar-item v-for="route in routes" :key="route.path" :item="route" :base-path="route.path" />
      </el-menu>
      <!--  -->
    </el-scrollbar>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import Logo from './Logo'
import Users from './Users'
import SidebarItem from './SidebarItem'
import themeJson from '@/assets/json/theme.json'

export default {
  components: { SidebarItem, Logo,Users },
  computed: {
    ...mapGetters([
      'sidebar'
    ]),
    routes() {
      // this.$router.options.routes  不加载addRouter挂上去的路由，因此不适用
      return this.$store.state.permission.routers
    },
    activeMenu() {
      const route = this.$route
      const { meta, path } = route
      // if set path, the sidebar will highlight the path you set
      if (meta.activeMenu) {
        return meta.activeMenu
      }
      return path
    },
    showLogo() {
      return this.$store.state.settings.sidebarLogo
    },
    variables() {
      var theme = this.$store.state.theme.activeName
      // console.log(themeJson[theme]["el-menu"])
      return  themeJson[theme]["el-menu"]
    },
    isCollapse() {
      return !this.sidebar.opened
    }
  }
}
</script>
