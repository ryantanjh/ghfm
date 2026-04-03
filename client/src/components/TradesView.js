import React, { useState, useEffect } from 'react';
import { Table, Card, Button, Space } from 'antd';
import { ReloadOutlined, DownloadOutlined } from '@ant-design/icons';
import axios from 'axios';

const TradesView = ({ refreshTrigger }) => {
  const [trades, setTrades] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchTrades = async () => {
    setLoading(true);
    try {
      const response = await axios.get('http://localhost:8000/trades');
      setTrades(response.data);
    } catch (error) {
      console.error('Failed to fetch trades:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTrades();
  }, [refreshTrigger]);

  const downloadTradeReport = async () => {
    try {
      const response = await axios.get('http://localhost:8000/trades/download', {
        responseType: 'blob',
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'trade_report.csv');
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Failed to download trade report:', error);
    }
  };

  const columns = [
    {
      title: 'Trade ID',
      dataIndex: 'trade_id',
      key: 'trade_id',
      width: 100,
    },
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
      title: 'Fill Price',
      dataIndex: 'fill_price',
      key: 'fill_price',
      width: 120,
      render: (price) => `$${price.toFixed(2)}`,
    },
    {
      title: 'Fill Quantity',
      dataIndex: 'fill_qty',
      key: 'fill_qty',
      width: 120,
    },
    {
      title: 'Timestamp',
      dataIndex: 'timestamp',
      key: 'timestamp',
      render: (timestamp) => new Date(timestamp).toLocaleString(),
    },
  ];

  return (
    <Card
      title="Trades"
      extra={
        <Space>
          <Button
            icon={<DownloadOutlined />}
            onClick={downloadTradeReport}
          >
            Download Report
          </Button>
          <Button
            icon={<ReloadOutlined />}
            onClick={fetchTrades}
            loading={loading}
          >
            Refresh
          </Button>
        </Space>
      }
    >
      <Table
        columns={columns}
        dataSource={trades}
        rowKey="trade_id"
        loading={loading}
        pagination={{ pageSize: 10 }}
      />
    </Card>
  );
};

export default TradesView;
