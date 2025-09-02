// StudyBloom API Service Layer
// Save this as: src/services/api.js or utils/api.js

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

class StudyBloomAPI {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  // Generic request method
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      credentials: 'include', // Important for session cookies
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.message || `HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('API Request failed:', error);
      throw error;
    }
  }

  // Authentication
  async login(username, password) {
    return this.request('/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
  }

  async register(username, email, password) {
    return this.request('/register', {
      method: 'POST',
      body: JSON.stringify({ username, email, password }),
    });
  }

  async logout() {
    return this.request('/logout', { method: 'GET' });
  }

  // Goals Management
  async getGoals() {
    return this.request('/api/goals');
  }

  async createGoal(goalData) {
    return this.request('/api/goals', {
      method: 'POST',
      body: JSON.stringify(goalData),
    });
  }

  async updateGoal(goalId, goalData) {
    return this.request(`/api/goals/${goalId}`, {
      method: 'PUT',
      body: JSON.stringify(goalData),
    });
  }

  async deleteGoal(goalId) {
    return this.request(`/api/goals/${goalId}`, {
      method: 'DELETE',
    });
  }

  // Tasks Management
  async getTasks() {
    return this.request('/api/tasks');
  }

  async createTask(taskData) {
    return this.request('/api/tasks', {
      method: 'POST',
      body: JSON.stringify(taskData),
    });
  }

  async updateTask(taskId, taskData) {
    return this.request(`/api/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(taskData),
    });
  }

  async deleteTask(taskId) {
    return this.request(`/api/tasks/${taskId}`, {
      method: 'DELETE',
    });
  }

  // Streaks & Analytics
  async getStreak() {
    return this.request('/api/streaks');
  }

  async updateStreak() {
    return this.request('/api/streaks/update', {
      method: 'POST',
    });
  }

  async getStreakAnalytics() {
    return this.request('/api/streaks/analytics');
  }

  // Study Sessions
  async getStudySessions() {
    return this.request('/api/study-sessions');
  }

  async startStudySession(sessionData) {
    return this.request('/api/study-sessions', {
      method: 'POST',
      body: JSON.stringify(sessionData),
    });
  }

  async endStudySession(sessionId) {
    return this.request(`/api/study-sessions/${sessionId}/end`, {
      method: 'PUT',
    });
  }

  // Rewards
  async getRewards() {
    return this.request('/api/rewards');
  }

  async getAvailableRewards() {
    return this.request('/api/rewards/available');
  }

  async checkRewardEligibility() {
    return this.request('/api/rewards/check-eligibility');
  }

  async redeemReward(rewardId) {
    return this.request(`/api/rewards/${rewardId}/redeem`, {
      method: 'POST',
    });
  }

  // Study Groups
  async getGroups() {
    return this.request('/api/groups');
  }

  async getAvailableGroups() {
    return this.request('/api/groups/available');
  }

  async createGroup(groupData) {
    return this.request('/api/groups', {
      method: 'POST',
      body: JSON.stringify(groupData),
    });
  }

  async joinGroup(groupId) {
    return this.request(`/api/groups/${groupId}/join`, {
      method: 'POST',
    });
  }

  async checkGroupEligibility() {
    return this.request('/api/groups/check-eligibility');
  }

  // Reminders
  async getReminders() {
    return this.request('/api/reminders');
  }

  async createReminder(reminderData) {
    return this.request('/api/reminders', {
      method: 'POST',
      body: JSON.stringify(reminderData),
    });
  }

  async getUpcomingReminders() {
    return this.request('/api/reminders/upcoming');
  }

  // AI Integration
  async generateAIResponse(input) {
    return this.request('/ai/generate', {
      method: 'POST',
      body: JSON.stringify({ input }),
    });
  }

  async getAIStatus() {
    return this.request('/ai/status');
  }
}

// Create and export a singleton instance
const api = new StudyBloomAPI();
export default api; 