import React, { useState } from "react";
import YouTube from "react-youtube";

const Home = () => {
  const [id, setId] = useState("");
  const [link, setLink] = useState("");
  var regExp =
    /^(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})/;

  const load = async (e) => {
    e.preventDefault();
    setId(document.getElementById("link").value.match(regExp));
    setLink(document.getElementById("link").value);
  };

  return (
    <section className="xl:padding-l wide:padding-r padding-b py-14">
      <div className="flex items-center justify-center">
        <div className="flex mt-6 space-y-0 bg-white shadow-2xl shadow-black rounded-2xl max-lg:flex-col max-lg:space-y-8">
          <div className="flex flex-col justify-center p-4 px-8 max-lg:p-8">
            <form onSubmit={load}>
              <div className="py-2">
                <label className="mb-2 text-md">Enter YouTube Link</label>
                <input
                  type="text"
                  name="link"
                  id="link"
                  className="w-full p-2 border border-gray-300 rounded-md placeholder:font-light placeholder:text-gray-500"
                ></input>

                <button
                  type="submit"
                  className="w-full bg-black text-white p-2 rounded-lg mb-3 mt-4 hover:bg-white hover:text-black hover:border-black hover:border-2"
                >
                  Submit
                </button>

                {/* Check if link is not empty before passing it to YouTube component */}
                {id && <YouTube videoId={id[1]} />}
              </div>
            </form>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Home;
