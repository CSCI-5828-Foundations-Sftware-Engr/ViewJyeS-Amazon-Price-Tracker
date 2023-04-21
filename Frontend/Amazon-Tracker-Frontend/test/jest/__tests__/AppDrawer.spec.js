import { describe, expect, it } from '@jest/globals';
import { installQuasarPlugin } from '@quasar/quasar-app-extension-testing-unit-jest';
import {mount, shallowMount} from '@vue/test-utils';
import AppDrawer from 'components/AppDrawer/AppDrawer.vue';

installQuasarPlugin();

describe("AppDrawer", () => {
  let wrapper;

  beforeEach(() => {
    wrapper = mount(AppDrawer);
  });

  afterEach(() => {
    wrapper.unmount();
  });

  it("renders the component", () => {
    expect(wrapper.exists()).toBe(true);
  });

  it("updates the isLoggedIn value when the user is authenticated", () => {
    wrapper.vm.$options.setup[0](); // call the onMounted hook
    expect(wrapper.vm.isLoggedIn).toBe(false); // initially not authenticated
    wrapper.vm.$options.setup[0].toReturn.onAuthStateChanged({
      uid: "abc123",
      email: "test@example.com",
    }); // simulate authentication
    expect(wrapper.vm.isLoggedIn).toBe(true); // should be authenticated now
  });

});

