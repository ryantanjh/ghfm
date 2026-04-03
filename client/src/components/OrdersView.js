import React, { useState, useEffect } from 'react';
import { Table, Card, Tag, Button } from 'antd';
import { ReloadOutlined } from '@ant-design/icons';
import axios from 'axios';

const OrdersView = ({ refreshTrigger }) => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchOrders = async () => {
    setLoading(true);
    try {
      const response = await axios.get('http://localhost:8000/orders');
      setOrders(response.data);
    } catch (error) {
      console.error('Failed to fetch orders:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchOrders();
  }, [refreshTrigger]);

  const getStatusColor = (status) => {
    const colorMap = {
      'NEW': 'blue',
      'SENT': 'cyan',
      'FILLED': 'green',
      'PARTIAL_FILL': 'orange',
      'REJECTED': 'red'
    };
    return colorMap[status] || 'default';
  };

  const columns = [
    {
      title: 'Order ID',
      dataIndex: 'order_id',
      key: 'order_id',
      width: 100,
    },
    {
      title: 'Broker',
      dataIndex: 'broker',
      key: 'broker',
      width: 100,
    },
    {
      title: 'Symbol',
      dataIndex: 'symbol',
      key: 'symbol',
      width: 100,
    },
    {
      title: 'Type',
      dataIndex: 'order_type',
      key: 'order_type',
      width: 100,
    },
    {
      title: 'Price',
      dataIndex: 'price',
      key: 'price',
      width: 100,
      render: (price) => `$${price.toFixed(2)}`,
    },
    {
      title: 'Quantity',
      dataIndex: 'qty',
      key: 'qty',
      width: 100,
    },
    {
      title: 'Status',
      dataIndex: 'order_status',
      key: 'order_status',
      width: 120,
      render: (status) => (
        <Tag color={getStatusColor(status)}>{status}</Tag>
      ),
    },
    {
      title: 'Rejection Reason',
      dataIndex: 'rejection_reason',
      key: 'rejection_reason',
      render: (reason) => reason || '-',
    },
  ];

  return (
    <Card
      title="Orders"
      extra={
        <Button
          icon={<ReloadOutlined />}
          onClick={fetchOrders}
          loading={loading}
        >
          Refresh
        </Button>
      }
    >
      <Table
        columns={columns}
        dataSource={orders}
        rowKey="order_id"
        loading={loading}
        pagination={{ pageSize: 10 }}
      />
    </Card>
  );
};

export default OrdersView;
