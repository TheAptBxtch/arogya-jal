import React from 'react';
import Head from 'next/head';
import Dashboard from '../components/Dashboard';

const HomePage: React.FC = () => {
  return (
    <>
      <Head>
        <title>ArogyaJal Predictive Maintenance</title>
        <meta name="description" content="Predictive maintenance system for water pumps" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main>
        <Dashboard />
      </main>
    </>
  );
};

export default HomePage;