import ProfileImage from '../components/Jackson';
import ProfileImageGreeny from '../components/Greenberg';
import ProfileImageDarsh from '../components/Adarsh';
import ProfileImageWyatt from '../components/Wyatt';
import Link from 'next/link';








export default function About() {
   return (
   // <div>
   //   <Header />
   //   <div className="p-8">
   //     <h1 className="text-2xl font-bold">About Us</h1>
   //     <p>Learn more about Longhorn Rooms and our mission to help students find study spaces on campus.</p>
   //   </div>
   //   {/* Jackson */}
   //     <div className="mt-8">
   //         <ProfileImage />
   //     </div>
   //     <div className="mt-8">
   //         <ProfileImageGreeny />
   //     </div>
   //     <div className="mt-8">
   //         <ProfileImageDarsh />
   //     </div>
   //     <div className="mt-8">
   //         <ProfileImageWyatt />
   //     </div>
   // </div>


 //   <div>
 //   <Header />
 //   <div className="p-8">
 //     <h1 className="text-2xl font-bold">About Us</h1>
 //     <p>Learn more about Longhorn Rooms and our mission to help students find study spaces on campus.</p>
 //   </div>
 //   <div className="image-container">
 //     <ProfileImage />
 //     <ProfileImageGreeny />
 //     <ProfileImageDarsh />
 //     <ProfileImageWyatt />
 //   </div>
 // </div>


 <div>
     <div className="p-8">
       <h1 className="text-2xl font-bold">About Us</h1>
       <br />
       <p>We are a team of four dedicated students who are passionate about making it easier to find study spaces on campus. We understand the challenges of finding an open room to focus, collaborate, or just get some quiet time. That is why we created Longhorn Rooms, an app designed to locate available study rooms across the UT campus in real time. Whether you’re looking for a quick spot to review notes or a quiet space for group work, our app is here to simplify your search and save you time.</p>
       <br />
       <Link
          href={{
            pathname: 'https://github.com/JackGreezy/longhorn-rooms/tree/master',
            query: { name: 'test' },
          }}
        >
          Click here to follow our project on GitHub
        </Link>
        <br />
        <br />
        <p>And click on our names to be directed to our Linkden</p>
     </div>

     {/* <div className="image-container">
       <div className="profile-item">
         <ProfileImage />
         <p className="caption">Jackson Price</p>
       </div>
       <div className="profile-item">
         <ProfileImageGreeny />
         <p className="caption">Jack Greenberg</p>
       </div>
       <div className="profile-item">
         <ProfileImageDarsh />
         <p className="caption">Adarsh Payyakkil</p>
       </div>
       <div className="profile-item">
         <ProfileImageWyatt />
         <p className="caption">Wyatt Hansen</p>
       </div>
         {/* <div className="profile-item">
         <ProfileImageWyatt src="/Wyatt.jpg" alt="Wyatt" />   
         <p className="caption">Wyatt</p>
         </div>
         </div> */}
   {/* </div>
   </div> */} 


   <div className="image-container">
  <div className="profile-item">
    <ProfileImage />
    <p className="caption">
      <Link
        href={{
          pathname: "https://www.linkedin.com/in/jacksonprice2", // Replace with the actual LinkedIn URL
        }}
        target="_blank" // Opens the link in a new tab
      >
        Jackson Price
      </Link>
    </p>
  </div>

  <div className="profile-item">
    <ProfileImageGreeny />
    <p className="caption">
      <Link
        href={{
          pathname: "https://www.linkedin.com/in/jack-greenberg-968885280/", // Replace with the actual LinkedIn URL
        }}
        target="_blank"
      >
        Jack Greenberg
      </Link>
    </p>
  </div>

  <div className="profile-item">
    <ProfileImageDarsh />
    <p className="caption">
      <Link
        href={{
          pathname: "https://www.linkedin.com/in/adarsh-payyakkil/", // Replace with the actual LinkedIn URL
        }}
        target="_blank"
      >
        Adarsh Payyakkil
      </Link>
    </p>
  </div>

  <div className="profile-item">
    <ProfileImageWyatt />
    <p className="caption">
      <Link
        href={{
          pathname: "https://www.linkedin.com/in/wyatt-c-hansen/", // Replace with the actual LinkedIn URL
        }}
        target="_blank"
      >
        Wyatt Hansen
      </Link>
    </p>
  </div>
</div>
</div>





 );
};
