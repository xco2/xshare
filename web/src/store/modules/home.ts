import { defineStore } from 'pinia'

type HomeType = {
  permissionLoading: boolean
  access: boolean
}

export const useHomeStore = defineStore('home', {
  state: (): HomeType => {
    return {
      permissionLoading: false,
      access: false,
    }
  },
  getters: {
    getPermissionLoading(): boolean {
      return this.permissionLoading
    },
    getPermissionAccess(): boolean {
      return this.access
    },
  },
  actions: {
    setPermissionLoading(status: boolean) {
      this.permissionLoading = status
    },
    setPermissionAccess(status: boolean) {
      this.access = status
    },
  },
})
