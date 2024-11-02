// pages/_app.tsx
import '../styles/globals.css';
import { AppProps } from 'next/app';
import Head from 'next/head';

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <>
      <Head>
        <link
          rel="stylesheet"
          href="https://js.arcgis.com/4.24/esri/themes/light/main.css"
        />
      </Head>
      <Component {...pageProps} />
    </>
  );
}

export default MyApp;
