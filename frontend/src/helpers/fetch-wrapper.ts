/* eslint-disable @typescript-eslint/no-explicit-any */
import { useAuthStore } from '@/stores'
import { getLoadingBar } from '@/helpers/loading-bar'
import { getMessageProvider } from '@/helpers/message'
import { error_messages } from './error_messages'

// helper functions to make API calls using fetch
// wrap fetch call and add loading bar

function requestWrapper<T extends (...args: any[]) => Promise<any>>(fetchFunction: T) {
  return async (...args: Parameters<T>): Promise<Awaited<ReturnType<T>>> => {
    const loadingBar = getLoadingBar()
    loadingBar?.start()
    try {
      const result = await fetchFunction(...args)
      loadingBar?.finish()
      return result
    } catch (error) {
      loadingBar?.error()
      throw error
    }
  }
}

// export HTTP methods

export const http = {
  get: requestWrapper(request('GET')),
  post: requestWrapper(request('POST')),
  put: requestWrapper(request('PUT')),
  delete: requestWrapper(request('DELETE')),
  form: requestWrapper(formRequest),
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
    const { logout } = useAuthStore()
    if ([401].includes(response.status)) {
      // auto logout if 401 Unauthorized response returned from api
      logout()
    }
    if ([403].includes(response.status)) {
      // show message if 403 Forbidden response returned from api redirect to 403 page
      window.location.href = '/403'
    }
    if ([404].includes(response.status)) {
      // redirect to 404 page
      window.location.href = '/404'
    }
    if ([500].includes(response.status)) {
      // redirect to 500 page
      window.location.href = '/500'
    }
    if ([400].includes(response.status)) {
      const messageProvider = getMessageProvider()
      messageProvider?.error(getFriendlyErrorMessage(data))
    }

    // get error message from body or default to response status
    return Promise.reject(getFriendlyErrorMessage(data))
  }

  return data
}

function getFriendlyErrorMessage(error: any): string {
  const error_code = error.detail.error_code
  if (error_code in error_messages) {
    return error_messages[error_code as keyof typeof error_messages]
  }
  return 'Ocurrió un error inesperado.'
}
