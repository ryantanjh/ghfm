import React from 'react';
import { Layout, Typography } from 'antd';
import 'antd/dist/reset.css';

const { Header, Content } = Layout;
const { Title } = Typography;

function App() {
  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{ background: '#001529', padding: '0 20px' }}>
        <Title level={3} style={{ color: 'white', margin: '16px 0' }}>
          Order Management System
        </Title>
      </Header>
      <Content style={{ padding: '20px' }}>
        <div style={{ background: '#fff', padding: '24px', minHeight: '80vh' }}>
          <Title level={4}>Welcome to OMS</Title>
          <p>Frontend architecture is ready.</p>
        </div>
      </Content>
    </Layout>
  );
}

export default App;
