import { shallowMount } from '@vue/test-utils'
import SearchTracker from 'layouts/SearchTracker.vue'

describe('SearchTracker.vue', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = shallowMount(SearchTracker);
  });

  afterEach(() => {
    wrapper.unmount();
  });

  it('renders the Amazon Link label', () => {
    expect(wrapper.find('.search-row-item-1').text()).toMatch('Amazon Link:');
  });

  it('updates text when input value changes', async () => {
    const input = wrapper.find('input');
    await input.setValue('https://www.amazon.com/dp/B08SBK64QH');
    expect(wrapper.vm.text).toBe('https://www.amazon.com/dp/B08SBK64QH');
  });

  it('sets priceDecrease to false when its toggle is clicked', async () => {
    const toggle1 = wrapper.find('.q-toggle:first-of-type');
    await toggle1.trigger('click');
    expect(wrapper.vm.priceDecrease).toBe(false);
  });

  it('sets everyHour to true when its toggle is clicked', async () => {
    const toggle2 = wrapper.find('.q-toggle:last-of-type');
    await toggle2.trigger('click');
    expect(wrapper.vm.everyHour).toBe(true);
  });

  it('displays an alert when track button is clicked and input is empty', async () => {
    window.alert = jest.fn();
    const trackBtn = wrapper.find('.q-btn');
    await trackBtn.trigger('click');
    expect(window.alert).toHaveBeenCalledWith('Enter a link');
  });

  // Mocking the API request
  const mockAxios = {
    put: jest.fn(() => Promise.resolve({ data: 'success' }))
  };

});
