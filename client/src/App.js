import React, { useState } from 'react';
import { Layout, Typography, Menu, Space } from 'antd';
import { FormOutlined, UnorderedListOutlined, LineChartOutlined } from '@ant-design/icons';
import 'antd/dist/reset.css';
import OrderForm from './components/OrderForm';
import OrdersView from './components/OrdersView';
import TradesView from './components/TradesView';

const { Header, Content } = Layout;
const { Title } = Typography;

function App() {
  const [currentPage, setCurrentPage] = useState('create-order');
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleOrderSubmitted = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  const menuItems = [
    {
      key: 'create-order',
      icon: <FormOutlined />,
      label: 'Create Order',
    },
    {
      key: 'orders',
      icon: <UnorderedListOutlined />,
      label: 'Orders',
    },
    {
      key: 'trades',
      icon: <LineChartOutlined />,
      label: 'Trades',
    },
  ];

  const renderContent = () => {
    switch (currentPage) {
      case 'create-order':
        return <OrderForm onOrderSubmitted={handleOrderSubmitted} />;
      case 'orders':
        return <OrdersView refreshTrigger={refreshTrigger} />;
      case 'trades':
        return <TradesView refreshTrigger={refreshTrigger} />;
      default:
        return <OrderForm onOrderSubmitted={handleOrderSubmitted} />;
    }
  };

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{ background: '#001529', padding: '0 20px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <Title level={3} style={{ color: 'white', margin: '16px 0' }}>
          Order Management System
        </Title>
        <Menu
          theme="dark"
          mode="horizontal"
          selectedKeys={[currentPage]}
          items={menuItems}
          onClick={({ key }) => setCurrentPage(key)}
          style={{ flex: 1, justifyContent: 'flex-end', minWidth: 0 }}
        />
      </Header>
      <Content style={{ padding: '20px' }}>
        <Space direction="vertical" size="large" style={{ width: '100%' }}>
          {renderContent()}
        </Space>
      </Content>
    </Layout>
  );
}

export default App;
