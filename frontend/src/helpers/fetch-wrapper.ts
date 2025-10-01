/* eslint-disable @typescript-eslint/no-explicit-any */
import { useAuthStore } from '@/stores'

export const http = {
  get: request('GET'),
  post: request('POST'),
  put: request('PUT'),
  delete: request('DELETE'),
  form: formRequest,
}

function request(method: 'GET' | 'POST' | 'PUT' | 'DELETE') {
  return (url: string, body?: any) => {
    const requestOptions: {
      method: string
      headers: { Authorization?: string; 'Content-Type'?: string }
      body?: string
    } = {
      method,
      headers: authHeader(url),
    }
    if (body) {
      requestOptions.headers['Content-Type'] = 'application/json'
      requestOptions.body = JSON.stringify(body)
    }
    return fetch(url, requestOptions).then(handleResponse)
  }
}

// Handle x-www-form-urlencoded data
function formRequest(method: 'POST' | 'PUT', url: string, body: any) {
  const requestOptions: {
    method: string
    headers: { Authorization?: string; 'Content-Type': string }
    body: string
  } = {
    method,
    headers: {
      ...authHeader(url),
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams(body).toString(),
  }
  return fetch(url, requestOptions).then(handleResponse)
}

// helper functions

function authHeader(url: string) {
  // return auth header with jwt if user is logged in and request is to the api url
  const { userToken: user } = useAuthStore()
  const isLoggedIn = !!user?.access_token
  const isApiUrl = url.startsWith(import.meta.env.VITE_API_URL)

  console.log('Auth Header - isLoggedIn:', isLoggedIn, 'isApiUrl:', isApiUrl)
  if (isLoggedIn && isApiUrl) {
    return { Authorization: `Bearer ${user.access_token}` }
  } else {
    return {}
  }
}

async function handleResponse(response: any) {
  const isJson = response.headers?.get('content-type')?.includes('application/json')
  let data = null
  if (isJson && response.status !== 204) {
    data = await response.json()
  }

  // check for error response
  if (!response.ok) {
    const { userToken: user, logout } = useAuthStore()
    if ([401, 403].includes(response.status) && user) {
      // auto logout if 401 Unauthorized or 403 Forbidden response returned from api
      logout()
    }

    // get error message from body or default to response status
    const error = (data && data.message) || response.status
    return Promise.reject(error)
  }

  return data
}
