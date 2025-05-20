import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    anonymousName: localStorage.getItem('anonymousName') || '',
    joinDate: localStorage.getItem('joinDate') || new Date().toISOString(),
    sessionId: localStorage.getItem('sessionId') || '',
    user_profile: null,
    exercise_plan: [],
    goal_duration: '1 month',
    painCheckDone: false
  }),
  actions: {
    setAnonymousName(name) {
      if (!name || name.trim().length < 2 || name.trim().length > 20) {
        throw new Error('昵称长度必须在2-20个字符之间')
      }
      if (name.toLowerCase().includes('admin')) {
        throw new Error('昵称不能包含admin相关字符')
      }
      this.anonymousName = name.trim()
      localStorage.setItem('anonymousName', this.anonymousName)
    },
    resetAnonymousName() {
      const prefix = 'User'
      const randomNum = Math.floor(Math.random() * 10000).toString().padStart(4, '0')
      const newName = `${prefix}${randomNum}`
      this.anonymousName = newName
      localStorage.setItem('anonymousName', newName)
    },
    resetSession() {
      const newSessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9)
      this.sessionId = newSessionId
      localStorage.setItem('sessionId', newSessionId)
    },
    setUserProfile(profile) {
      this.user_profile = profile
    },
    setExercisePlan(plan) {
      this.exercise_plan = plan
    },
    setGoalDuration(duration) {
      this.goal_duration = duration
    },
    setPainCheckDone(done) {
      this.painCheckDone = done
    }
  }
})

// 持久化配置
useUserStore.persist = true 