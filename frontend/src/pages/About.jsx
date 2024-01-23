import React from 'react'

const About = () => {
  return (
    <section className="xl:padding-l wide:padding-r padding-b py-14">
      <div className="container mx-auto mt-8 text-white font-montserrat leading-normal text-lg px-2 rounded-sm h-full hover:underline hover:underline-offset-4 hover:decoration-[#4986d6] hover:translate-x-1">
        <h1 className="text-3xl font-bold mb-4">About Our Website</h1>

        <p className="mb-4">
          Welcome to our website! We are a team of four passionate individuals
          who came together to create a platform that transforms YouTube videos
          into informative PDF summaries.
        </p>

        <h2 className="text-2xl font-bold mb-2">Meet the Team</h2>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <h3 className="text-xl font-semibold mb-2">Web Development Team</h3>
            <p>Deep Kasodariya</p>
            <p>Ayush Gulhane</p>
          </div>

          <div>
            <h3 className="text-xl font-semibold mb-2">
              Machine Learning Team
            </h3>
            <p>Nishit Kekane</p>
            <p>Aditya Yedurkar</p>
          </div>
        </div>

        <h2 className="text-2xl font-bold mt-8 mb-2">Our Technology Stack</h2>

        <p>
          Our website is built using the MERN stack (MongoDB, Express.js, React,
          Node.js) for seamless integration of front-end and back-end
          components. The user interface is designed with Tailwind CSS to
          provide a clean and modern look.
        </p>
      </div>
    </section>
  );
}

export default About
