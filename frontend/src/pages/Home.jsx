import React, { useEffect, useState } from 'react'
import Card from '../components/Card'
import useAuth from '../hooks/useAuth'
import axiosClient from '../api/axiosClient'

const Home = () => {
  const [urls, setUrls] = useState()
  const { auth } = useAuth()

  const fetchUrls = async () => {
    if (auth) {
      const resp = await axiosClient.get('/api/v1/video/get')
      let data = resp.data
      setUrls(data)
    }
  }

  const handleRemove = async (id) => {
    await axiosClient.delete(`/api/v1/video/deleteUrl/${id}`)
    fetchUrls()
  }

  const handleDownload = (id) => {
    console.log('Download:', id)
    // Add logic to handle download
  }

  useEffect(() => {
    fetchUrls()
  }, [])

  return (
    <section className="xl:padding-l wide:padding-r padding-b py-14">
      {/* Displaying the urls. */}
      <div className="container mx-auto p-4">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {urls?.map((video) => (
            <Card
              key={video.videoId}
              title={video.title}
              description={video.description}
              thumbnailUrl={video.thumbnailUrl}
              onRemove={() => handleRemove(video._id)}
              onDownload={() => handleDownload(video._id)}
            />
          ))}
        </div>
      </div>
    </section>
  )
}

export default Home
