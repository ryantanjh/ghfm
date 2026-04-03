import React, { useState } from 'react';
import { Form, Input, Button, Select, InputNumber, message, Card } from 'antd';
import axios from 'axios';

const { Option } = Select;

const OrderForm = ({ onOrderSubmitted }) => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (values) => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/send_limit_order', {
        broker: values.broker,
        symbol: values.symbol,
        order_type: 'LIMIT',
        price: values.price,
        qty: values.qty
      });

      message.success(`Order created successfully! Order ID: ${response.data.order_id}`);
      form.resetFields();

      if (onOrderSubmitted) {
        onOrderSubmitted();
      }
    } catch (error) {
      message.error(`Failed to create order: ${error.response?.data?.detail || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card title="Create Limit Order" style={{ maxWidth: 600, margin: '0 auto' }}>
      <Form
        form={form}
        layout="vertical"
        onFinish={handleSubmit}
        initialValues={{
          broker: 'IBKR',
          order_type: 'LIMIT'
        }}
      >
        <Form.Item
          label="Broker"
          name="broker"
          rules={[{ required: true, message: 'Please select a broker' }]}
        >
          <Select>
            <Option value="IBKR">IBKR</Option>
          </Select>
        </Form.Item>

        <Form.Item
          label="Symbol"
          name="symbol"
          rules={[{ required: true, message: 'Please select a symbol' }]}
        >
          <Select placeholder="Select a symbol">
            <Option value="AAPL">AAPL</Option>
            <Option value="DBS">DBS</Option>
          </Select>
        </Form.Item>

        <Form.Item
          label="Order Type"
          name="order_type"
        >
          <Select disabled>
            <Option value="LIMIT">LIMIT</Option>
          </Select>
        </Form.Item>

        <Form.Item
          label="Price"
          name="price"
          rules={[{ required: true, message: 'Please enter a price' }]}
        >
          <InputNumber
            min={0.01}
            step={0.01}
            precision={2}
            style={{ width: '100%' }}
            placeholder="e.g., 100.50"
          />
        </Form.Item>

        <Form.Item
          label="Quantity"
          name="qty"
          rules={[{ required: true, message: 'Please enter a quantity' }]}
        >
          <InputNumber
            min={1}
            step={1}
            style={{ width: '100%' }}
            placeholder="e.g., 1000"
          />
        </Form.Item>

        <Form.Item>
          <Button type="primary" htmlType="submit" loading={loading} block>
            Submit Order
          </Button>
        </Form.Item>
      </Form>
    </Card>
  );
};

export default OrderForm;
