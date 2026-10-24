import axios from 'axios';

// Abstracted Base API Client
// All endpoint URLs, ports, and headers are encapsulated within this service layer.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

const http = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiClient = {
  // Authentication & User Profile Services
  auth: {
    login: async (email, password) => {
      const response = await http.post('/auth/login', { email, password });
      return response.data;
    },
    register: async (email, password, fullName) => {
      const response = await http.post('/auth/register', {
        email,
        password,
        full_name: fullName,
      });
      return response.data;
    },
    updateProfile: async (userId, profileData) => {
      const response = await http.put(`/auth/profile/${userId}`, profileData);
      return response.data;
    },
  },

  // Meal & Vision AI Estimation Services
  meals: {
    estimate: async (description, imageFile) => {
      const formData = new FormData();
      if (description) formData.append('description', description);
      if (imageFile) formData.append('image', imageFile);

      const response = await http.post('/meals/estimate', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      return response.data;
    },
    logMeal: async (mealData) => {
      const response = await http.post('/meals/log', mealData);
      return response.data;
    },
    getHistory: async (userId = 1) => {
      const response = await http.get(`/meals/history/${userId}`);
      return response.data;
    },
  },

  // Packaged Food & Barcode Scanner Services
  food: {
    scanBarcodeImage: async (imageFile) => {
      const formData = new FormData();
      formData.append('image', imageFile);
      const response = await http.post('/packaged-food/scan-barcode', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      return response.data;
    },
    lookupBarcode: async (barcode) => {
      const response = await http.get(`/packaged-food/lookup/${barcode}`);
      return response.data;
    },
    searchProducts: async (query) => {
      const response = await http.get(`/packaged-food/search`, {
        params: { query },
      });
      return response.data;
    },
    compareProducts: async (originalProduct, alternativeProduct) => {
      const response = await http.post('/packaged-food/compare', {
        original_product: originalProduct,
        alternative_product: alternativeProduct,
      });
      return response.data;
    },
    findHealthyAlternatives: async (productQuery) => {
      const formData = new FormData();
      formData.append('product_query', productQuery);
      const response = await http.post('/packaged-food/compare-alternatives', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      return response.data;
    },
  },
};

export default apiClient;
